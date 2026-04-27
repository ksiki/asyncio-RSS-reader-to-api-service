from typing import Final

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str


class BaseApiPrefixes(BaseSettings):
    api_version: str


settings: Final[Settings] = Settings(api_prefix="/api")
