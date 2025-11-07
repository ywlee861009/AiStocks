from types import SimpleNamespace
from urllib.parse import quote_plus

import pytest

from stock_analyzer.scrapers.news.google_news_strategy import GoogleNewsRssStrategy


class DummyEntry:
    def __init__(self, title, link, published="N/A", source_title=None):
        self.title = title
        self.link = link
        self._published = published
        self.source = SimpleNamespace(title=source_title) if source_title else None

    def get(self, key, default=None):
        if key == "published":
            return self._published
        return default


def test_google_news_strategy_fetch_news_limits_results(mocker):
    """뉴스 항목이 전략의 limit만큼만 반환되는지 확인한다."""

    entries = [
        DummyEntry("뉴스1", "https://example.com/1", "2024-01-01", "매체1"),
        DummyEntry("뉴스2", "https://example.com/2", "2024-01-02", "매체2"),
    ]

    mock_feed = SimpleNamespace(entries=entries)
    mock_parse = mocker.patch(
        "stock_analyzer.scrapers.news.google_news_strategy.feedparser.parse",
        return_value=mock_feed,
    )

    strategy = GoogleNewsRssStrategy(query_limit=1)

    result = strategy.fetch_news("삼성전자")

    assert result == [
        {
            "title": "뉴스1",
            "link": "https://example.com/1",
            "pub_date": "2024-01-01",
            "source": "매체1",
        }
    ]

    expected_url = GoogleNewsRssStrategy.BASE_URL + quote_plus("삼성전자")
    mock_parse.assert_called_once_with(expected_url)


def test_google_news_strategy_returns_empty_on_exception(mocker):
    """feedparser에서 예외가 발생하면 빈 리스트를 반환한다."""

    mocker.patch(
        "stock_analyzer.scrapers.news.google_news_strategy.feedparser.parse",
        side_effect=Exception("parse error"),
    )

    strategy = GoogleNewsRssStrategy(query_limit=5)

    assert strategy.fetch_news("카카오") == []

