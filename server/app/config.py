import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./interview_agent.db"
    SECRET_KEY: str = "your-super-secret-key-change-in-production-abc123xyz"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    LLM_PROVIDER: str = "mock"  # mock, openai, gemini
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
