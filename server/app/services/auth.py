from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def register_user(db: AsyncSession, user_create: UserCreate) -> User:
    # Check if exists
    db_user = await get_user_by_username(db, user_create.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_email = await get_user_by_email(db, user_create.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_pw
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Initialize user progress on registration
    from app.services.progress_service import get_or_create_progress
    await get_or_create_progress(db, user.id)
    
    return user

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(oauth2_scheme)) -> User:
    # Actually we get_db in endpoint, let's create a custom depend to get user
    pass

# Direct helper to retrieve active user from token
async def verify_token_and_get_user(db: AsyncSession, token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
        
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
