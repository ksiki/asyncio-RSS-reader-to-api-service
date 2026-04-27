from contextlib import asynccontextmanager
from typing import Final

from fastapi import FastAPI

from api_service.src.api.v1.api import api_router as api_v1
from api_service.src.core.config import settings
from common.tkq import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()
    yield
    await broker.shutdown()


app: Final[FastAPI] = FastAPI(lifespan=lifespan)

app.include_router(
    router=api_v1,
    prefix=settings.api_prefix,
    tags=[settings.api_prefix + api_v1.prefix],
)
