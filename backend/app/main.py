from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .database import get_db
from .config import current_config
from .services.key_analyzer import KeyAnalyzer
from .models import User
from .auth import (
    Token,
    User as UserSchema,
    create_access_token,
    get_current_active_user,
    get_password_hash,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
)
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
import uuid
from .utils.debug import debug


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str


app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # 开发服务器
        "http://127.0.0.1:5173",  # 也支持 localhost 的 IP 形式
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    debug.log(f"Generated token for user {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
    debug.log(f"Getting user info for: {current_user.username}")
    return current_user


@app.get("/keys/recent")
async def get_recent_keys(
    current_user: UserSchema = Depends(get_current_active_user),
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return analyzer.get_recent_keys(start_time=start, end_time=end)


@app.get("/keys/high-score")
async def get_high_score_keys(
    current_user: UserSchema = Depends(get_current_active_user),
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return analyzer.get_high_score_keys(start_time=start, end_time=end)


@app.get("/statistics")
async def get_statistics(
    current_user: UserSchema = Depends(get_current_active_user),
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return analyzer.get_statistics(start_time=start, end_time=end)


@app.post("/auth/register")
async def register(user_data: RegisterUser, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # 创建新用户
    user = User(
        id=str(uuid.uuid4()),
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}
