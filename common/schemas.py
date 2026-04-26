from datetime import date, time
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    IN_QUEUE = "in queue"
    IN_PROGRESS = "in progress"
    SUCCESS = "success"
    FAILURE = "failure"


class Filters(BaseModel):
    count_rows: int = Field(default=15, ge=1, le=150)
    start_date: Optional[date] = None
    start_time: Optional[time] = None
    end_date: Optional[date] = None
    end_time: Optional[time] = None


class RSSItem(BaseModel):
    title: str
    link: str
    summary: Optional[str] = None
    pub_date: Optional[str] = None
    author: Optional[str] = None


class TaskCfg(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_id: str
    rss: str
    filters: Filters


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_id: str
    task_status: TaskStatus
    data: list[RSSItem] = Field(default_factory=list)
    error: Optional[str] = None
