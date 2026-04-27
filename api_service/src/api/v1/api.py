from typing import Final

from fastapi import APIRouter

from api_service.src.api.v1.core.config import v1_api_prefixes
from api_service.src.api.v1.endpoints.data_holder import router as data_holder_router
from api_service.src.api.v1.endpoints.parser import router as parser_router

api_router: Final[APIRouter] = APIRouter(prefix=v1_api_prefixes.api_version)

api_router.include_router(router=parser_router, prefix=v1_api_prefixes.parser)
api_router.include_router(router=data_holder_router, prefix=v1_api_prefixes.data_holder)
