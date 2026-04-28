from datetime import date

import pytest

from common.schemas import RSSItem
from rss_reader.core.processor import processor


@pytest.fixture
def xml() -> str:
    xml = """<?xml version="1.0" encoding="UTF-8" ?>
            <rss version="2.0">
            <channel>
                <item>
                    <title>new1</title>
                    <link>http://example.com/1</link>
                    <description>Description for new1</description>
                    <pubDate>Mon, 27 Apr 2026 12:00:00 +0000</pubDate>
                    <author>example@example.com (Example Examplovich)</author>
                </item>

                <item>
                    <link>http://example.com/2</link>
                    <description>Not exists title and autor</description>
                    <pubDate>Tue, 28 Apr 2026 10:00:00 +0000</pubDate>
                </item>

                <item>
                    <title>Not exists link, autor and description</title>
                    <pubDate>Tue, 28 Apr 2026 11:00:00 +0000</pubDate>
                </item>
            </channel>
            </rss>"""
    return xml


class TestPrecossor:
    def test_parse(self, xml) -> None:
        items: list[RSSItem] = processor.parse(xml)

        assert len(items) == 3

        assert items[0].title == "new1"
        assert items[0].link == "http://example.com/1"
        assert items[0].description == "Description for new1"
        assert items[0].pub_date == date(year=2026, month=4, day=27)
        assert items[0].author == "example@example.com (Example Examplovich)"

        assert items[1].title == "No Title"
        assert items[1].author == "Unknown"

        assert items[2].link == ""
        assert items[2].description == ""
