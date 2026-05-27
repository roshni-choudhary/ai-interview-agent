from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services import auth as auth_service
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth_service.register_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(auth_service.oauth2_scheme)
):
    user = await auth_service.verify_token_and_get_user(db, token)
    return user
