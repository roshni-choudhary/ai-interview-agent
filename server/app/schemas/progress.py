from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional

class TopicScore(BaseModel):
    solved: int
    attempted: int
    avg_score: float

class RoadmapItem(BaseModel):
    topic: str
    priority: str  # high, medium, low
    reason: str
    suggested_count: int
    difficulty: str

class ProgressResponse(BaseModel):
    total_sessions: int
    total_problems_solved: int
    total_problems_attempted: int
    current_streak: int
    longest_streak: int
    last_active: Optional[datetime] = None
    topic_scores: Dict[str, TopicScore]
    difficulty_distribution: Dict[str, int]
    weak_topics: List[str]
    strong_topics: List[str]
    roadmap: List[RoadmapItem]

    class Config:
        from_attributes = True

class DashboardData(BaseModel):
    progress: ProgressResponse
    recent_sessions: List[Dict[str, Any]]
    topic_breakdown: List[Dict[str, Any]]
    streak_data: Dict[str, Any]
