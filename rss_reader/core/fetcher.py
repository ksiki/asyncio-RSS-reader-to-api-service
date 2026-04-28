import logging
from typing import Final, Optional

import httpx

from common.config import settings

logger = logging.getLogger(__name__)


class RSSFetcher:
    __slots__ = ("_client", "_timeout")

    def __init__(self, timeout: float):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={"User-Agent": "RSS-Bot/1.0 (Compatibility: Mozilla/5.0)"},
        )

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    @client.setter
    def client(self, value) -> httpx.AsyncClient:
        raise AttributeError("Can't set attribute 'client'")

    async def fetch(self, url: str) -> Optional[str]:
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            logger.error(
                msg=f"HTTP error {e.response.status_code} while fetching {url}"
            )
            raise e
        except httpx.RequestError as e:
            logger.error(
                msg=f"An error occurred while requesting {e.request.url!r}: {e}"
            )
            raise e
        except Exception as e:
            logger.exception(msg=f"Unexpected error fetching RSS from {url}: {e}")
            raise e

    async def close(self) -> None:
        await self.client.aclose()


fetcher: Final[RSSFetcher] = RSSFetcher(timeout=settings.fetch_timeout)
