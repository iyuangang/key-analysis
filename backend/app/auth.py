from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import get_db
from . import models
from .utils.redis import redis_client
from .utils.debug import debug

# 配置
SECRET_KEY = "your-secret-key"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
USER_CACHE_TTL = 300  # 用户缓存5分钟

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True  # 允许从 ORM 模型创建 Pydantic 模型


class UserInDB(User):
    hashed_password: str


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(db: AsyncSession, username: str):
    # 尝试从缓存获取用户
    cache_key = f"user:{username}"
    debug.log(f"Attempting to get user from cache: {username}")
    cached_user = redis_client.get(cache_key)
    if cached_user:
        debug.log(f"User cache hit: {username}")
        return models.User(**cached_user)

    debug.log(f"User cache miss: {username}")
    result = await db.execute(
        select(models.User).where(models.User.username == username)
    )
    user = result.scalar_one_or_none()
    if user:
        # 缓存用户数据
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "disabled": user.disabled,
            "hashed_password": user.hashed_password,
        }
        debug.log(f"Caching user data for: {username}")
        redis_client.set(cache_key, user_data, ttl=USER_CACHE_TTL)
        debug.log(f"User data cached successfully for: {username}")
    return user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    # 尝试从缓存获取认证结果
    cache_key = f"auth:{username}:{get_password_hash(password)}"
    debug.log(f"Attempting to get auth result from cache: {username}")
    cached_result = redis_client.get(cache_key)
    if cached_result is not None:
        debug.log(f"Auth cache hit: {username}")
        return models.User(**cached_result) if cached_result else False

    debug.log(f"Auth cache miss: {username}")
    user = await get_user(db, username)
    if not user:
        debug.log(f"User not found: {username}")
        redis_client.set(cache_key, None, ttl=USER_CACHE_TTL)
        return False
    if not verify_password(password, user.hashed_password):
        debug.log(f"Invalid password for user: {username}")
        redis_client.set(cache_key, None, ttl=USER_CACHE_TTL)
        return False

    # 缓存认证结果
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "disabled": user.disabled,
        "hashed_password": user.hashed_password,
    }
    debug.log(f"Caching auth result for: {username}")
    redis_client.set(cache_key, user_data, ttl=USER_CACHE_TTL)
    debug.log(f"Auth result cached successfully for: {username}")
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 尝试从缓存获取token解析结果
    cache_key = f"token:{token}"
    cached_user = redis_client.get(cache_key)
    if cached_user:
        debug.log(f"Token cache hit")
        return User(**cached_user)

    debug.log(f"Token cache miss")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    async for db in get_db():
        try:
            user = await get_user(db, username=token_data.username)
            if user is None:
                raise credentials_exception

            # 缓存token解析结果
            user_data = {
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "disabled": user.disabled,
            }
            redis_client.set(cache_key, user_data, ttl=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
            return User(**user_data)
        finally:
            await db.close()

    raise credentials_exception


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
