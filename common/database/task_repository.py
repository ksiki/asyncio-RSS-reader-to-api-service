from typing import Final, Optional

from common.database.core.redis_service import redis_service
from common.schemas import RSSItem, Task, TaskStatus


class TaskRepository:
    def __init__(self, redis_service):
        self.redis = redis_service
        self.prefix = "task:"

    async def save(self, task: Task) -> None:
        await self.redis.set_model(f"{self.prefix}{task.task_id}", task)

    async def get(self, task_id: str) -> Optional[Task]:
        return await self.redis.get_model(
            f"{self.prefix}{task_id}", 
            Task
        )

    async def update_date(self, task_id:str, data: list[RSSItem]) -> None:
        task = await self.get(task_id)
        if task:
            task.data = data
            await self.save(task)

    async def update_status(self, task_id: str, status: TaskStatus, error: str = None) -> None:
        task = await self.get(task_id)
        if task:
            task.task_status = status
            if error:
                task.error = error
            await self.save(task)


task_repository: Final[TaskRepository] = TaskRepository(
    redis_service=redis_service
)
