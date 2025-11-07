import pytest

from stock_analyzer.scrapers.company.company_scraper import TopCompaniesScraper
from stock_analyzer.scrapers.enums import CompanyScrapeSource


def test_top_companies_scraper_delegates_to_strategy(mocker):
    """전략 클래스가 올바르게 초기화되고 호출되는지 확인한다."""

    mock_strategy_cls = mocker.patch(
        "stock_analyzer.scrapers.company.company_scraper.NaverFinanceStrategy"
    )
    mock_strategy_instance = mock_strategy_cls.return_value
    mock_strategy_instance.scrape.return_value = ["기업A", "기업B"]

    scraper = TopCompaniesScraper(top_n=2)

    result = scraper.get_top_companies(CompanyScrapeSource.NAVER_FINANCE)

    assert result == ["기업A", "기업B"]
    mock_strategy_cls.assert_called_once_with(2)
    mock_strategy_instance.scrape.assert_called_once()


def test_top_companies_scraper_raises_for_invalid_source():
    """등록되지 않은 소스 요청 시 ValueError를 발생시킨다."""

    scraper = TopCompaniesScraper(top_n=1)

    with pytest.raises(ValueError) as excinfo:
        scraper.get_top_companies(object())

    assert "지원하지 않는 소스" in str(excinfo.value)

