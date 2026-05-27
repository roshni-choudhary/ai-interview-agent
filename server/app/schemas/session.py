from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional

class SessionCreate(BaseModel):
    topics: Optional[List[str]] = None
    difficulty: Optional[str] = "easy"

class MessageCreate(BaseModel):
    content: str
    message_type: Optional[str] = "chat"

class SessionMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    message_type: str
    metadata_json: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    id: int
    user_id: int
    status: str
    difficulty: str
    topics: Optional[List[str]] = None
    score: Optional[float] = None
    total_questions: int
    correct_answers: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    messages: Optional[List[SessionMessageResponse]] = None

    class Config:
        from_attributes = True

class CodeSubmission(BaseModel):
    code: str
    language: str

class HintRequest(BaseModel):
    pass

class SessionSummary(BaseModel):
    session_id: int
    score: float
    total_questions: int
    correct_answers: int
    topics: List[str]
    difficulty: str
    duration_seconds: int
