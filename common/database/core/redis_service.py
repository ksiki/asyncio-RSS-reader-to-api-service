import logging
from typing import Final, Optional, Type, TypeVar

import redis.asyncio as redis
from pydantic import BaseModel
from redis import Redis

from common.config import settings
from common.database.core.exceptions import ParseException

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)


class RedisService:
    __slots__ = ("_redis",)

    def __init__(self, redis_url: str):
        self._redis = redis.from_url(redis_url, decode_responses=True)

    @property
    def redis(self) -> Redis:
        return self._redis

    @redis.setter
    def redis(self, value) -> Redis:
        raise AttributeError("Can't set attribute 'redis'")

    async def set_model(
        self, key: str, model: BaseModel, expire: int = settings.auto_del_msg
    ) -> None:
        await self.redis.set(name=key, value=model.model_dump_json(), ex=expire)

    async def get_model(self, key: str, model_type: Type[T]) -> Optional[T]:
        raw_data = await self.redis.get(key)
        if not raw_data:
            logger.warning(msg=f"Model with key={key} is not exists")
            return None
        try:
            return model_type.model_validate_json(raw_data)
        except Exception as e:
            logger.error(msg=f"Parse JSON into {model_type.__name__}. Error: {e}")
            raise ParseException()

    async def close(self) -> None:
        await self.redis.close()


redis_service: Final[RedisService] = RedisService(redis_url=settings.redis_url)
