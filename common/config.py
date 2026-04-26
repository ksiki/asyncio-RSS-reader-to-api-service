import logging
from typing import Final
from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    broker_url: str
    redis_url: str
    max_parsing_time: int
    debug: bool


settings: Final[Settings] = Settings(
    broker_url=config("BROKER_URL"),
    redis_url=config("REDIS_URL"),
    max_parsing_time=15,
    debug=config("DEBUG", default=False, cast=bool)
)

log_level = logging.DEBUG if settings.debug else logging.WARNING
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
