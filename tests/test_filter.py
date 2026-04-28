from datetime import date

import pytest

from common.schemas import Filters, RSSItem
from rss_reader.core.filter import filter


@pytest.fixture
def rss_items() -> list[RSSItem]:
    items = [
        RSSItem(
            title="title_1", link="link_1", pub_date=date(year=2026, month=4, day=22)
        ),
        RSSItem(
            title="title_2", link="link_2", pub_date=date(year=2026, month=4, day=27)
        ),
        RSSItem(
            title="title_3", link="link_3", pub_date=date(year=2026, month=4, day=14)
        ),
        RSSItem(
            title="title_4", link="link_4", pub_date=date(year=2026, month=4, day=20)
        ),
        RSSItem(
            title="title_5", link="link_5", pub_date=date(year=2026, month=4, day=23)
        ),
        RSSItem(
            title="title_6", link="link_6", pub_date=date(year=2026, month=4, day=22)
        ),
    ]
    return items


@pytest.fixture
def filters() -> Filters:
    return Filters(
        count_rows=3,
        start_date=date(year=2026, month=4, day=20),
        end_date=date(year=2026, month=4, day=27),
    )


class TestFilter:
    def test_apply_filters(self, rss_items, filters) -> None:
        filtered_data = filter.apply_filters(rss_items, **filters.model_dump())

        assert len(filtered_data) == 3
        assert filtered_data[0].title == "title_2"
        assert filtered_data[1].title == "title_5"
        assert filtered_data[2].title == "title_6"
