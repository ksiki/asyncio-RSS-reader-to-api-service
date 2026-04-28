from contextlib import asynccontextmanager
from typing import Final

from fastapi import FastAPI

from api_service.src.api.v1.api import api_router as api_v1
from api_service.src.core.config import settings
from common.database.core.redis_service import redis_service
from common.tkq import broker
from rss_reader.core.fetcher import fetcher


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()
    yield
    await broker.shutdown()
    await redis_service.close()
    await fetcher.close()


app: Final[FastAPI] = FastAPI(lifespan=lifespan)

app.include_router(
    router=api_v1,
    prefix=settings.api_prefix,
    tags=[settings.api_prefix + api_v1.prefix],
)
