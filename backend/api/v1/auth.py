"""
認證 API 端點
處理用戶註冊、登錄和 token 驗證
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from ...database.base import get_db
from ...models.user import User
from ...core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

# OAuth2 密碼流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Pydantic 模型
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# 輔助函數
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """根據用戶名獲取用戶"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """根據郵箱獲取用戶"""
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """驗證用戶"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """獲取當前用戶"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="無法驗證憑證",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """獲取當前活躍用戶"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用戶已被停用")
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """獲取當前管理員用戶"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="權限不足，需要管理員權限"
        )
    return current_user


# API 端點
@router.post("/auth/register", response_model=UserResponse, tags=["auth"])
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    用戶註冊

    - **username**: 用戶名（唯一）
    - **email**: 郵箱（唯一）
    - **password**: 密碼
    """
    # 檢查用戶名是否已存在
    if get_user_by_username(db, user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用戶名已存在"
        )

    # 檢查郵箱是否已存在
    if get_user_by_email(db, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="郵箱已被註冊"
        )

    # 創建新用戶
    hashed_password = get_password_hash(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/auth/login", response_model=Token, tags=["auth"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用戶登錄

    - **username**: 用戶名
    - **password**: 密碼

    返回 JWT access token
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用戶名或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用戶已被停用"
        )

    # 創建 access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=UserResponse, tags=["auth"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    獲取當前用戶信息

    需要認證
    """
    return current_user


@router.get("/auth/verify", tags=["auth"])
async def verify_token_endpoint(current_user: User = Depends(get_current_active_user)):
    """
    驗證 token 是否有效

    需要認證
    """
    return {"valid": True, "username": current_user.username}
