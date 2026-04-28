from typing import Final

import atoma

from common.schemas import RSSItem


class RSSProcessor:
    @staticmethod
    def parse(xml_content: str) -> list[RSSItem]:
        feed = atoma.parse_rss_bytes(xml_content.encode("utf-8"))
        return [
            RSSItem(
                title=item.title or "No Title",
                link=item.link or "",
                pub_date=item.pub_date.date(),
                description=item.description or "",
                author=item.author or "Unknown",
            )
            for item in feed.items
        ]


processor: Final[RSSProcessor] = RSSProcessor()
