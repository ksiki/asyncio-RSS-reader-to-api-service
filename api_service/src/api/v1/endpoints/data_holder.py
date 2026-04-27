from typing import Final

from fastapi import APIRouter

from api_service.src.api.v1.core import services

router: Final[APIRouter] = APIRouter()


@router.get("/status/{task_id}/")
async def check_status(tasl_id: str) -> None:
    return await services.check_task_status(task_id=tasl_id)


@router.get("/data/{task_id}/")
async def get_date(task_id: str) -> None:
    return await services.get_parse_result(task_id=task_id)
