from typing import Final
from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    broker_url: str
    redis_url: str
    debug: bool


settings: Final[Settings] = Settings(
    broker_url=config("BROKER_URL"),
    redis_url=config("REDIS_URL"),
    debug=config("DEBUG")
)
