from typing import Final

from taskiq_aio_pika import AioPikaBroker

from common.config import settings
from common.database.task_repository import task_repository
from common.schemas import RSSItem, TaskCfg, TaskStatus
from rss_reader import parser


broker: Final[AioPikaBroker] = AioPikaBroker(url=settings.broker_url)


@broker.task
async def handle_task(data_dict: dict) -> None:
    try:
        task_cfg = TaskCfg.model_validate(data_dict)

        await task_repository.update_status(
            task_id=task_cfg.task_id,
            status=TaskStatus.IN_PROGRESS
        )
    
        items: list[RSSItem] = await parser.parse(task_cfg.rss) 
        
        await task_repository.update_date(
            task_id=task_cfg.task_id, 
            data=items)
        await task_repository.update_status(
            task_id=task_cfg.task_id, 
            status=TaskStatus.SUCCESS)
    except Exception as e:
        await task_repository.update_status(
            task_id=task_cfg.task_id,
            status=TaskStatus.FAILURE,
            error=str(e)
        )
        raise e
