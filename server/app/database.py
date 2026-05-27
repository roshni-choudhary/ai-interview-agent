from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings
from typing import AsyncGenerator

engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        # Import models here to register them with Base metadata
        from app.models.user import User
        from app.models.session import InterviewSession, SessionMessage
        from app.models.question import QuestionAttempt
        from app.models.progress import UserProgress
        
        await conn.run_sync(Base.metadata.create_all)
