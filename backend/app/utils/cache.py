from functools import wraps
from typing import Optional, Callable
import hashlib
import json
from .redis import redis_client
from .debug import debug


def cache(prefix: str, ttl: Optional[int] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            key_parts = [prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key = hashlib.md5(":".join(key_parts).encode()).hexdigest()

            # 尝试从缓存获取
            cached_result = redis_client.get(cache_key)
            if cached_result is not None:
                debug.log(f"Cache hit for function {func.__name__}")
                return json.loads(cached_result)

            # 执行函数
            debug.log(f"Cache miss for function {func.__name__}")
            result = await func(*args, **kwargs)

            # 缓存结果
            redis_client.set(cache_key, json.dumps(result), ttl=ttl)
            return result

        return wrapper

    return decorator
