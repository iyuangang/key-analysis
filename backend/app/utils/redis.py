from redis.client import Redis
from typing import Optional, Any
import json
from ..config import current_config
from .debug import debug

redis_config = current_config.get("redis", {})
if not redis_config:
    debug.error("Redis configuration is empty")


class RedisClient:
    def __init__(self):
        self.enabled = True
        try:
            host = redis_config.get("host")
            port = redis_config.get("port")
            if not host or not port:
                raise ValueError(f"Invalid Redis config - host: {host}, port: {port}")

            self.client = Redis(
                host=host,
                port=port,
                password=redis_config.get("password"),
                db=redis_config.get("db", 0),
                decode_responses=True,
            )
            # 测试连接
            self.client.ping()
            debug.log(f"Redis connected successfully to {host}:{port}")
        except Exception as e:
            debug.error(f"Redis connection failed: {str(e)}")
            debug.error(f"Redis config: {redis_config}")
            self.enabled = False
        self.prefix = redis_config.get("prefix", "key_analyzer:")
        self.ttl = redis_config.get("ttl", 3600)  # 默认缓存1小时
        debug.log(f"Redis initialized with prefix: {self.prefix}, ttl: {self.ttl}")

    def _get_key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    def get(self, key: str) -> Optional[Any]:
        if not self.enabled:
            debug.log("Redis is disabled")
            return None
        try:
            data = self.client.get(self._get_key(key))
            if data:
                debug.log(f"Cache hit for key: {key}, value length: {len(data)}")
                return json.loads(data)
            debug.log(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            debug.error(f"Redis get error for key {key}: {str(e)}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if not self.enabled:
            debug.log("Redis is disabled")
            return False
        try:
            key = self._get_key(key)
            data = json.dumps(value)
            debug.log(f"Attempting to cache data with key: {key}, size: {len(data)}")
            self.client.set(key, data, ex=ttl or self.ttl)
            debug.log(
                f"Successfully cached data with key: {key}, ttl: {ttl or self.ttl}"
            )
            return True
        except Exception as e:
            debug.error(f"Redis set error for key {key}: {str(e)}")
            debug.error(f"Failed data: {str(value)[:100]}...")
            return False

    def delete(self, key: str) -> bool:
        if not self.enabled:
            return False
        try:
            self.client.delete(self._get_key(key))
            debug.log(f"Cache delete: {key}")
            return True
        except Exception as e:
            debug.error(f"Redis delete error: {e}")
            return False

    def clear_prefix(self, prefix: str) -> bool:
        if not self.enabled:
            return False
        try:
            pattern = f"{self.prefix}{prefix}*"
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
                debug.log(f"Cache clear pattern: {pattern}")
            return True
        except Exception as e:
            debug.error(f"Redis clear pattern error: {e}")
            return False


redis_client = RedisClient()
