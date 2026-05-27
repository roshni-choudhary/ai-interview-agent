from typing import Dict, Any, List, Optional
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.agent.llm_provider import get_llm_provider
from app.agent.question_bank import select_next_question, get_question
from app.agent.code_evaluator import CodeEvaluator
from app.agent.hint_generator import HintGenerator
from app.agent.feedback_generator import FeedbackGenerator
from app.agent.difficulty_adapter import DifficultyAdapter
from app.services.session_service import add_message, record_attempt
from app.services.progress_service import update_progress_after_attempt, get_or_create_progress
from app.models.session import InterviewSession, SessionMessage
from app.models.question import QuestionAttempt

class InterviewAgent:
    def __init__(self, provider_name: str):
        self.llm = get_llm_provider(provider_name)
        self.code_evaluator = CodeEvaluator()
        self.hint_generator = HintGenerator(self.llm)
        self.feedback_generator = FeedbackGenerator(self.llm)
        self.difficulty_adapter = DifficultyAdapter()

    async def get_initial_greeting(self, session: InterviewSession) -> str:
        prompt = (
            f"Generate a professional coding interviewer greeting. Let the candidate know "
            f"we are practicing coding topics: {', '.join(session.topics or [])} on {session.difficulty} difficulty."
        )
        system = "You are a professional software engineer coding interviewer."
        return await self.llm.generate(prompt, system)

    async def present_question(self, question: Dict[str, Any]) -> str:
        # Construct message content presenting the problem
        description = question.get("description", "")
        examples_str = ""
        for i, ex in enumerate(question.get("examples", [])):
            examples_str += f"\n**Example {i+1}**:\nInput: `{ex['input']}`\nOutput: `{ex['output']}`\nExplanation: {ex['explanation']}\n"
            
        constraints_str = "\n".join([f"- {c}" for c in question.get("constraints", [])])
        
        content = (
            f"### 📝 Problem: {question['title']} ({question['difficulty'].capitalize()})\n\n"
            f"{description}\n\n"
            f"#### Examples:\n{examples_str}\n"
            f"#### Constraints:\n{constraints_str}\n\n"
            f"I have initialized your coding window with the starter template. Please write your solution and click 'Run Tests' or submit your response once ready!"
        )
        return content

    async def generate_chat_response(self, question: Dict[str, Any], user_msg: str, chat_history: List[Dict[str, Any]]) -> str:
        # Create dialog prompt
        history_formatted = ""
        for msg in chat_history[-6:]:  # past 6 messages for context
            history_formatted += f"{msg['role']}: {msg['content']}\n"
            
        prompt = (
            f"You are conducting a live technical interview for the problem: {question['title']}.\n"
            f"Description: {question['description']}\n\n"
            f"Chat History:\n{history_formatted}"
            f"User: {user_msg}\n"
            f"Interviewer response:"
        )
        system = "You are a professional, helpful, but rigorous software engineer coding interviewer. Guide the user without giving away the direct solution."
        return await self.llm.generate(prompt, system)

# Module level convenience functions
async def start_interview_session(db: AsyncSession, session_id: int, user_id: int) -> Dict[str, Any]:
    session_res = await db.execute(select(InterviewSession).where(InterviewSession.id == session_id))
    session = session_res.scalars().first()
    if not session:
        return {"error": "Session not found"}
        
    agent = InterviewAgent("mock")
    greeting = await agent.get_initial_greeting(session)
    await add_message(db, session_id, "assistant", greeting, "chat")
    
    # Auto-load and present the first question based on selected topics
    progress = await get_or_create_progress(db, user_id)
    attempted_res = await db.execute(select(QuestionAttempt.question_id).where(QuestionAttempt.user_id == user_id))
    attempted_ids = [r[0] for r in attempted_res.all()]
    
    question = select_next_question(progress.topic_scores or {}, attempted_ids, session.topics)
    if not question:
        return {"error": "No questions available"}
        
    presentation = await agent.present_question(question)
    
    # Store current question context in system/message metadata
    metadata = {
        "question_id": question["id"],
        "title": question["title"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "starter_code": question["starter_code"]
    }
    
    await add_message(db, session_id, "assistant", presentation, "question", metadata)
    
    return {
        "status": "success",
        "greeting": greeting,
        "question": {
            "id": question["id"],
            "title": question["title"],
            "description": question["description"],
            "constraints": question["constraints"],
            "examples": question["examples"],
            "starter_code": question["starter_code"],
            "topic": question["topic"],
            "difficulty": question["difficulty"]
        }
    }

async def process_interview_message(db: AsyncSession, session_id: int, user_id: int, message: str) -> Dict[str, Any]:
    session_res = await db.execute(select(InterviewSession).where(InterviewSession.id == session_id))
    session = session_res.scalars().first()
    if not session:
        return {"error": "Session not found"}
        
    # Get last question metadata to know what problem we are currently on
    msgs_res = await db.execute(
        select(SessionMessage)
        .where(SessionMessage.session_id == session_id)
        .order_by(SessionMessage.created_at.desc())
    )
    messages = msgs_res.scalars().all()
    
    current_q_id = None
    for msg in messages:
        if msg.message_type == "question" and msg.metadata_json:
            current_q_id = msg.metadata_json.get("question_id")
            break
            
    if not current_q_id:
        current_q_id = "two_sum"  # default fallback
        
    question = get_question(current_q_id)
    agent = InterviewAgent("mock")
    
    history = [{"role": m.role, "content": m.content} for m in reversed(messages[:10])]
    reply = await agent.generate_chat_response(question, message, history)
    
    saved_msg = await add_message(db, session_id, "assistant", reply, "chat")
    return {
        "id": saved_msg.id,
        "role": "assistant",
        "content": reply,
        "message_type": "chat"
    }

async def submit_code(db: AsyncSession, session_id: int, user_id: int, code: str, language: str) -> Dict[str, Any]:
    session_res = await db.execute(select(InterviewSession).where(InterviewSession.id == session_id))
    session = session_res.scalars().first()
    if not session:
        return {"error": "Session not found"}
        
    # Find current question
    msgs_res = await db.execute(
        select(SessionMessage)
        .where(SessionMessage.session_id == session_id)
        .order_by(SessionMessage.created_at.desc())
    )
    messages = msgs_res.scalars().all()
    
    question_meta = None
    for msg in messages:
        if msg.message_type == "question" and msg.metadata_json:
            question_meta = msg.metadata_json
            break
            
    if not question_meta:
        return {"error": "No active question found to submit code against."}
        
    question = get_question(question_meta["question_id"])
    agent = InterviewAgent("mock")
    
    # 1. Run tests
    eval_res = await agent.code_evaluator.evaluate(code, language, question["test_cases"], question["id"])
    
    # 2. Get feedback review
    feedback = await agent.feedback_generator.generate_feedback(question, code, language, eval_res)
    
    # Determine correctness
    is_correct = eval_res.get("all_passed", False)
    
    # Count hints used in session
    hints_used = sum([1 for m in messages if m.message_type == "hint"])
    
    # 3. Record attempt
    attempt_payload = {
        "question_id": question["id"],
        "question_title": question["title"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "user_code": code,
        "language": language,
        "is_correct": is_correct,
        "hints_used": hints_used,
        "time_spent_seconds": 300,  # rough placeholder or trackable
        "score": feedback.get("score", 70.0),
        "feedback": feedback.get("overall", ""),
        "test_results": eval_res
    }
    
    attempt = await record_attempt(db, session_id, user_id, attempt_payload)
    
    # 4. Update user profile aggregates & roadmap
    await update_progress_after_attempt(db, user_id, attempt)
    
    # 5. Post feedback to chat
    await add_message(db, session_id, "assistant", feedback.get("overall", ""), "feedback", {
        "score": feedback.get("score"),
        "is_correct": is_correct,
        "test_results": eval_res
    })
    
    # Determine dynamic next topic/difficulty & question selection
    progress = await get_or_create_progress(db, user_id)
    attempted_res = await db.execute(select(QuestionAttempt.question_id).where(QuestionAttempt.user_id == user_id))
    attempted_ids = [r[0] for r in attempted_res.all()]
    
    # Adapt difficulty up/down
    attempts_res = await db.execute(select(QuestionAttempt).where(QuestionAttempt.session_id == session_id))
    recent_attempts = [{"score": a.score, "hints_used": a.hints_used} for a in attempts_res.scalars().all()]
    
    next_diff = agent.difficulty_adapter.calculate_next_difficulty(recent_attempts, session.difficulty)
    session.difficulty = next_diff
    await db.commit()
    
    next_q = select_next_question(progress.topic_scores or {}, attempted_ids, session.topics)
    
    presentation = ""
    next_q_payload = None
    if next_q:
        presentation = await agent.present_question(next_q)
        next_metadata = {
            "question_id": next_q["id"],
            "title": next_q["title"],
            "topic": next_q["topic"],
            "difficulty": next_q["difficulty"],
            "starter_code": next_q["starter_code"]
        }
        await add_message(db, session_id, "assistant", presentation, "question", next_metadata)
        next_q_payload = {
            "id": next_q["id"],
            "title": next_q["title"],
            "description": next_q["description"],
            "constraints": next_q["constraints"],
            "examples": next_q["examples"],
            "starter_code": next_q["starter_code"],
            "topic": next_q["topic"],
            "difficulty": next_q["difficulty"]
        }
        
    return {
        "evaluation": eval_res,
        "feedback": feedback,
        "next_question": next_q_payload,
        "next_difficulty": next_diff
    }

async def request_hint(db: AsyncSession, session_id: int, user_id: int) -> Dict[str, Any]:
    msgs_res = await db.execute(
        select(SessionMessage)
        .where(SessionMessage.session_id == session_id)
        .order_by(SessionMessage.created_at.desc())
    )
    messages = msgs_res.scalars().all()
    
    question_meta = None
    for msg in messages:
        if msg.message_type == "question" and msg.metadata_json:
            question_meta = msg.metadata_json
            break
            
    if not question_meta:
        return {"error": "No active question found to offer hints."}
        
    question = get_question(question_meta["question_id"])
    agent = InterviewAgent("mock")
    
    # Calculate hint level based on number of hints already delivered in the session
    hint_count = sum([1 for m in messages if m.message_type == "hint"])
    next_hint_level = hint_count + 1
    
    hint_text = await agent.hint_generator.get_hint(question, next_hint_level)
    
    saved_msg = await add_message(db, session_id, "assistant", hint_text, "hint", {"hint_level": next_hint_level})
    
    return {
        "id": saved_msg.id,
        "role": "assistant",
        "content": hint_text,
        "message_type": "hint",
        "hint_level": next_hint_level
    }
