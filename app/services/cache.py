import hashlib
import json
from collections.abc import Awaitable, Callable
from typing import Any

from redis.asyncio import Redis

from app.integrations.redis_client import get_redis

Serializer = Callable[[Any], str]
Deserializer = Callable[[str], Any]


def default_serializer(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def default_deserializer(raw: str) -> Any:
    return json.loads(raw)


def default_key_builder(*args: Any, **kwargs: Any) -> str:
    raw = json.dumps({"args": args, "kwargs": kwargs}, ensure_ascii=False, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def cacheable(
    ttl: int,
    key_builder: Callable[..., str] | None = None,
    namespace: str = "default",
    serializer: Serializer = default_serializer,
    deserializer: Deserializer = default_deserializer,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            redis: Redis = get_redis()
            key_fn = key_builder or default_key_builder
            cache_key = f"{namespace}:{key_fn(*args, **kwargs)}"
            cached = await redis.get(cache_key)
            if cached is not None:
                return deserializer(cached)
            result = await func(*args, **kwargs)
            await redis.set(cache_key, serializer(result), ex=ttl)
            return result

        return wrapper

    return decorator
