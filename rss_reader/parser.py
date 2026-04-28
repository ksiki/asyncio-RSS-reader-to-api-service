import logging
from typing import Final

from common.schemas import Filters, RSSItem
from rss_reader.core.fetcher import fetcher
from rss_reader.core.filter import filter
from rss_reader.core.processor import processor

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def parse(rss: str, filters: Filters) -> list[RSSItem]:
    try:
        content = await fetcher.fetch(rss)
        result = processor.parse(content)
        result = filter.apply_filters(data=result, **filters.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error fetching {rss}: {e}")
        raise e
