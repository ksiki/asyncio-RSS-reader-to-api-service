from typing import Final, Optional, Type, TypeVar

import redis.asyncio as redis
from pydantic import BaseModel

from common.config import settings
from common.database.core.exceptions import ParseException


T = TypeVar("T", bound=BaseModel)


class RedisService:
    def __init__(self, redis_url: str):
        self._redis = redis.from_url(
            redis_url, 
            decode_responses=True
        )

    async def set_model(self, key: str, model: BaseModel, expire: int = 3600) -> None:
        await self._redis.set(
            name=key, 
            value=model.model_dump_json(), 
            ex=expire)

    async def get_model(self, key: str, model_type: Type[T]) -> Optional[T]:
        raw_data = await self._redis.get(key)
        if not raw_data:
            return None
        try:
            return model_type.model_validate_json(raw_data)
        except Exception as e:
            raise ParseException(f"Error: parse JSON into {model_type.__name__}")

    async def close(self) -> None:
        await self._redis.close()


redis_service: Final[RedisService] = RedisService(
    redis_url=settings.redis_url
)
