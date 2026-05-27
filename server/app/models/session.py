from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="active")  # active, completed, abandoned
    difficulty = Column(String, default="easy")  # easy, medium, hard
    topics = Column(JSON, nullable=True)  # List of topics/tags configured
    score = Column(Float, nullable=True)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    config = Column(JSON, nullable=True)  # custom configuration options

class SessionMessage(Base):
    __tablename__ = "session_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    message_type = Column(String, default="chat")  # chat, code, hint, feedback, question
    metadata_json = Column(JSON, nullable=True)  # dynamic helper payload
    created_at = Column(DateTime(timezone=True), server_default=func.now())
