from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.progress import ProgressResponse, DashboardData
from app.services import auth as auth_service
from app.services import progress_service
from typing import Any

router = APIRouter(prefix="/api/progress", tags=["progress"])

async def get_user_from_token(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(auth_service.oauth2_scheme)
):
    return await auth_service.verify_token_and_get_user(db, token)

@router.get("", response_model=ProgressResponse)
async def get_progress(
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    return await progress_service.get_or_create_progress(db, user.id)

@router.get("/dashboard", response_model=DashboardData)
async def get_dashboard(
    user: Any = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    return await progress_service.get_dashboard_data(db, user.id)
