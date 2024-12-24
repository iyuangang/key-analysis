from fastapi import Request, HTTPException
from ..utils.redis import redis_client
import time


async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    # 获取当前请求次数
    current = redis_client.get(key) or 0
    if int(current) >= 100:  # 每分钟最多100次请求
        raise HTTPException(status_code=429, detail="Too many requests")

    # 更新请求次数
    redis_client.set(key, int(current) + 1, ttl=60)

    response = await call_next(request)
    return response
