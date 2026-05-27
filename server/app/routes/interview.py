from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.session import SessionCreate, SessionResponse, SessionMessageResponse, MessageCreate, CodeSubmission, SessionSummary
from app.services import auth as auth_service
from app.services import session_service
from app.agent import orchestrator as agent_orchestrator
from typing import List, Dict, Any

router = APIRouter(prefix="/api/interview", tags=["interview"])

async def get_user_from_token(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(auth_service.oauth2_scheme)
):
    return await auth_service.verify_token_and_get_user(db, token)

@router.post("/start", response_model=SessionResponse)
async def start_session(
    config: SessionCreate,
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.create_session(db, user.id, config)
    # Start agent and present question
    agent_res = await agent_orchestrator.start_interview_session(db, session.id, user.id)
    if "error" in agent_res:
        raise HTTPException(status_code=400, detail=agent_res["error"])
        
    # Re-fetch session to populate messages
    session_with_msgs = await session_service.get_session(db, session.id, user.id)
    messages = await session_service.get_messages(db, session.id)
    session_with_msgs.messages = messages
    return session_with_msgs

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session_details(
    session_id: int,
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.get_session(db, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = await session_service.get_messages(db, session_id)
    session.messages = messages
    return session

@router.post("/{session_id}/message", response_model=SessionMessageResponse)
async def send_message(
    session_id: int,
    payload: MessageCreate,
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.get_session(db, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Record user message
    await session_service.add_message(db, session_id, "user", payload.content, payload.message_type)
    
    # Process with AI Interview Agent
    agent_reply = await agent_orchestrator.process_interview_message(db, session_id, user.id, payload.content)
    if "error" in agent_reply:
        raise HTTPException(status_code=400, detail=agent_reply["error"])
        
    return agent_reply

@router.post("/{session_id}/submit")
async def submit_solution(
    session_id: int,
    submission: CodeSubmission,
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.get_session(db, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Record user code in a user message
    user_code_block = f"Submitted solution in {submission.language}:\n```\n{submission.code}\n```"
    await session_service.add_message(db, session_id, "user", user_code_block, "code")
    
    res = await agent_orchestrator.submit_code(db, session_id, user.id, submission.code, submission.language)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
        
    return res

@router.post("/{session_id}/hint", response_model=SessionMessageResponse)
async def get_hint(
    session_id: int,
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    session = await session_service.get_session(db, session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    await session_service.add_message(db, session_id, "user", "Can I get a hint, please?", "chat")
    
    hint_res = await agent_orchestrator.request_hint(db, session_id, user.id)
    if "error" in hint_res:
        raise HTTPException(status_code=400, detail=hint_res["error"])
        
    return hint_res

@router.post("/{session_id}/end", response_model=SessionSummary)
async def end_session(
    session_id: int,
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    summary = await session_service.end_session(db, session_id, user.id)
    if not summary:
        raise HTTPException(status_code=404, detail="Session not found")
    return summary
