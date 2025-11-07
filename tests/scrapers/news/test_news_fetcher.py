import pytest

from stock_analyzer.scrapers.enums import NewsFetchSource
from stock_analyzer.scrapers.news.news_fetcher import NewsFetcher


def test_news_fetcher_delegates_to_strategy(mocker):
    """전략 클래스 생성과 fetch 호출이 올바르게 수행된다."""

    mock_strategy_cls = mocker.patch(
        "stock_analyzer.scrapers.news.news_fetcher.GoogleNewsRssStrategy"
    )
    mock_strategy_instance = mock_strategy_cls.return_value
    mock_strategy_instance.fetch_news.return_value = [
        {"title": "뉴스", "link": "https://example.com", "pub_date": "N/A", "source": "N/A"}
    ]

    fetcher = NewsFetcher(limit_per_company=3)

    result = fetcher.get_news("삼성전자", NewsFetchSource.GOOGLE_NEWS_RSS)

    assert result == mock_strategy_instance.fetch_news.return_value
    mock_strategy_cls.assert_called_once_with(3)
    mock_strategy_instance.fetch_news.assert_called_once_with("삼성전자")


def test_news_fetcher_raises_for_invalid_source():
    """등록되지 않은 소스일 경우 ValueError를 발생시킨다."""

    fetcher = NewsFetcher(limit_per_company=1)

    with pytest.raises(ValueError) as excinfo:
        fetcher.get_news("네이버", object())

    assert "지원하지 않는 뉴스 소스" in str(excinfo.value)

