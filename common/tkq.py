import asyncio
import logging
from typing import Final

from taskiq_aio_pika import AioPikaBroker

from common.config import settings
from common.database.task_repository import task_repository
from common.schemas import RSSItem, TaskCfg, TaskStatus
from rss_reader import parser

broker: Final[AioPikaBroker] = AioPikaBroker(url=settings.broker_url)
logger = logging.getLogger(__name__)


@broker.task
async def handle_task(data_dict: dict) -> None:
    task_id = data_dict.get("task_id", "unknown")

    try:
        task_cfg = TaskCfg.model_validate(data_dict)

        await task_repository.update_status(
            task_id=task_id, status=TaskStatus.IN_PROGRESS
        )
        logger.info(
            msg=f"Update status={TaskStatus.IN_PROGRESS} with task_id={task_id}"
        )

        items: list[RSSItem] = await asyncio.wait_for(
            parser.parse(task_cfg.rss, task_cfg.filters),
            timeout=settings.max_parsing_time,
        )
        await asyncio.sleep(60)

        await task_repository.update_data(task_id=task_id, data=items)
        logger.info(msg=f"Update data with task_id={task_id}")
        await task_repository.update_status(task_id=task_id, status=TaskStatus.SUCCESS)
        logger.info(
            msg=f"Update status={TaskStatus.IN_PROGRESS} with task_id={task_id}"
        )
    except Exception as e:
        await task_repository.update_status(
            task_id=task_id, status=TaskStatus.FAILURE, error=str(e)
        )
        raise e
