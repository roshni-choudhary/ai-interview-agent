from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_sessions = Column(Integer, default=0)
    total_problems_solved = Column(Integer, default=0)
    total_problems_attempted = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_active = Column(DateTime(timezone=True), nullable=True)
    topic_scores = Column(JSON, default=dict)  # {"arrays": {"solved": 5, "attempted": 6, "avg_score": 85.0}}
    difficulty_distribution = Column(JSON, default=dict)  # {"easy": 10, "medium": 5, "hard": 1}
    weak_topics = Column(JSON, default=list)  # ["graphs", "heaps"]
    strong_topics = Column(JSON, default=list)  # ["arrays", "strings"]
    roadmap = Column(JSON, default=list)  # Recommended next steps
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
