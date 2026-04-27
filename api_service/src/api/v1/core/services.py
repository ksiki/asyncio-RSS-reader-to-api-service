import logging
import uuid

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from common.database.task_repository import task_repository
from common.schemas import Filters, RSSItem, Task, TaskCfg, TaskStatus
from common.tkq import handle_task

logger = logging.getLogger(__name__)


async def create_new_task(rss: str, filters: Filters) -> JSONResponse:
    task_id = str(uuid.uuid4())
    logger.info(msg=f"Start to create new task. Id={task_id}")

    task = Task(task_id=task_id, task_status=TaskStatus.IN_QUEUE)
    await task_repository.save(task=task)
    logger.info(msg=f"Save new task. Id={task_id}")

    task_cfg = TaskCfg(task_id=task_id, rss=rss, filters=filters)
    await handle_task.kiq(task_cfg.model_dump())

    logger.info(msg=f"Task success created. Id={task_id}")
    return JSONResponse(content={"task_id": task_id})


async def check_task_status(task_id: str) -> JSONResponse:
    task: Task = await task_repository.get(task_id=task_id)
    return JSONResponse(
        content={"task_id": task_id, "status": task.task_status, "error": task.error}
    )


async def get_parse_result(task_id: str) -> list[RSSItem]:
    task: Task = task_repository.get(task_id=task_id)
    if task.task_status != TaskStatus.SUCCESS:
        error = (
            f"Task '{task_id}' is not finished yet (current status: {task.task_status})"
        )
        logger.error(msg=error)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return task.data
