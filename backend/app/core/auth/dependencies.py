from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...models.user import User
from ...core.db import get_db
from ...utils.redis import redis_client
from ...utils.debug import debug
from .security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import TokenData, UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
USER_CACHE_TTL = 300  # 用户缓存5分钟


async def get_user(db: AsyncSession, username: str) -> Optional[User]:
    cache_key = f"user:{username}"
    debug.log(f"Attempting to get user from cache: {username}")
    cached_user = redis_client.get(cache_key)
    if cached_user:
        debug.log(f"User cache hit: {username}")
        return User(**cached_user)

    debug.log(f"User cache miss: {username}")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user:
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


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    cache_key = f"token:{token}"
    cached_user = redis_client.get(cache_key)
    if cached_user:
        debug.log(f"Token cache hit")
        return UserResponse(**cached_user)

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

            user_data = {
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "disabled": user.disabled,
            }
            redis_client.set(cache_key, user_data, ttl=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
            return UserResponse(**user_data)
        finally:
            await db.close()

    raise credentials_exception


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
