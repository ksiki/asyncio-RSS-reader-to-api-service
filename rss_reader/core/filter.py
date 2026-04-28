from datetime import date
from typing import Final

from common.schemas import RSSItem


class RSSFilter:
    @staticmethod
    def apply_filters(
        data: list[RSSItem],
        count_rows: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list[RSSItem]:
        if start_date:
            data = [item for item in data if item.pub_date >= start_date]
        if end_date:
            data = [item for item in data if item.pub_date <= end_date]

        data.sort(key=lambda x: (x.pub_date, x.title), reverse=True)
        return data[:count_rows]


filter: Final[RSSFilter] = RSSFilter()
