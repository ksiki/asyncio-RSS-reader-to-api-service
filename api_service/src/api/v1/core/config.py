from typing import Final

from api_service.src.core.config import BaseApiPrefixes


class v1ApiPrefixes(BaseApiPrefixes):
    parser: str
    data_holder: str


v1_api_prefixes: Final[v1ApiPrefixes] = v1ApiPrefixes(
    api_version="/v1", parser="/parser", data_holder="/data-holder"
)
