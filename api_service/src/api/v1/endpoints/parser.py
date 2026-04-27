from typing import Annotated, Final

from fastapi import APIRouter, Body

from api_service.src.api.v1.core import services
from common.schemas import Filters

router: Final[APIRouter] = APIRouter()


@router.post("/")
async def parse_rss(rss: str, filters: Annotated[Filters, Body()] = Filters()) -> None:
    return await services.create_new_task(rss=rss, filters=filters)
