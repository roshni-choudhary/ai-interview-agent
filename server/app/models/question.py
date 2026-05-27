from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.database import Base

class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String, nullable=False)
    question_title = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    user_code = Column(Text, nullable=True)
    language = Column(String, default="python")
    is_correct = Column(Boolean, nullable=True)
    hints_used = Column(Integer, default=0)
    time_spent_seconds = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    test_results = Column(JSON, nullable=True)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())
