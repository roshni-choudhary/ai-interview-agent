from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.session import InterviewSession, SessionMessage
from app.models.question import QuestionAttempt
from app.schemas.session import SessionCreate, SessionSummary
from datetime import datetime
from typing import List, Dict, Any, Optional

async def create_session(db: AsyncSession, user_id: int, config: SessionCreate) -> InterviewSession:
    session = InterviewSession(
        user_id=user_id,
        status="active",
        difficulty=config.difficulty or "easy",
        topics=config.topics or ["arrays", "strings"],
        total_questions=0,
        correct_answers=0
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def get_session(db: AsyncSession, session_id: int, user_id: int) -> Optional[InterviewSession]:
    result = await db.execute(select(InterviewSession).where(
        InterviewSession.id == session_id,
        InterviewSession.user_id == user_id
    ))
    return result.scalars().first()

async def get_user_sessions(db: AsyncSession, user_id: int, limit: int = 10, offset: int = 0) -> List[InterviewSession]:
    result = await db.execute(select(InterviewSession)
        .where(InterviewSession.user_id == user_id)
        .order_by(desc(InterviewSession.started_at))
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())

async def add_message(
    db: AsyncSession, 
    session_id: int, 
    role: str, 
    content: str, 
    message_type: str = "chat", 
    metadata_json: Optional[Dict[str, Any]] = None
) -> SessionMessage:
    msg = SessionMessage(
        session_id=session_id,
        role=role,
        content=content,
        message_type=message_type,
        metadata_json=metadata_json
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def get_messages(db: AsyncSession, session_id: int) -> List[SessionMessage]:
    result = await db.execute(select(SessionMessage)
        .where(SessionMessage.session_id == session_id)
        .order_by(SessionMessage.created_at)
    )
    return list(result.scalars().all())

async def record_attempt(
    db: AsyncSession, 
    session_id: int, 
    user_id: int, 
    attempt_data: Dict[str, Any]
) -> QuestionAttempt:
    attempt = QuestionAttempt(
        session_id=session_id,
        user_id=user_id,
        question_id=attempt_data.get("question_id"),
        question_title=attempt_data.get("question_title"),
        topic=attempt_data.get("topic"),
        difficulty=attempt_data.get("difficulty"),
        user_code=attempt_data.get("user_code"),
        language=attempt_data.get("language", "python"),
        is_correct=attempt_data.get("is_correct"),
        hints_used=attempt_data.get("hints_used", 0),
        time_spent_seconds=attempt_data.get("time_spent_seconds"),
        score=attempt_data.get("score"),
        feedback=attempt_data.get("feedback"),
        test_results=attempt_data.get("test_results")
    )
    db.add(attempt)
    
    # Update Session statistics
    session_res = await db.execute(select(InterviewSession).where(InterviewSession.id == session_id))
    session = session_res.scalars().first()
    if session:
        session.total_questions = (session.total_questions or 0) + 1
        if attempt_data.get("is_correct"):
            session.correct_answers = (session.correct_answers or 0) + 1
        
    await db.commit()
    await db.refresh(attempt)
    return attempt

async def end_session(db: AsyncSession, session_id: int, user_id: int) -> Optional[SessionSummary]:
    session = await get_session(db, session_id, user_id)
    if not session:
        return None
    
    session.status = "completed"
    session.ended_at = datetime.utcnow()
    
    # Calculate score
    attempts_res = await db.execute(select(QuestionAttempt).where(QuestionAttempt.session_id == session_id))
    attempts = attempts_res.scalars().all()
    
    total_score = 0.0
    count = len(attempts)
    for a in attempts:
        total_score += (a.score or 0.0)
    
    session.score = (total_score / count) if count > 0 else 0.0
    await db.commit()
    
    duration = int((session.ended_at - session.started_at).total_seconds())
    
    return SessionSummary(
        session_id=session.id,
        score=session.score,
        total_questions=session.total_questions,
        correct_answers=session.correct_answers,
        topics=session.topics or [],
        difficulty=session.difficulty,
        duration_seconds=duration
    )
