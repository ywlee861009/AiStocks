import pytest
import requests

from stock_analyzer.scrapers.company.naver_strategy import NaverFinanceStrategy


@pytest.fixture
def mock_naver_html():
    """네이버 금융 페이지의 가짜 (축약된) HTML을 반환합니다."""
    return """
    <html>
        <body>
            <table class="type_2">
                <tbody>
                    <tr><td><a class="tltle">가짜전자</a></td></tr>
                    <tr><td><a class="tltle">가짜하이닉스</a></td></tr>
                    <tr><td><a class="tltle">가짜에너지솔루션</a></td></tr>
                    <tr><td><a class="tltle">가짜바이오</a></td></tr>
                </tbody>
            </table>
        </body>
    </html>
    """


@pytest.fixture
def mock_requests_get_success(mocker, mock_naver_html):
    """requests.get을 성공 응답으로 모킹합니다."""

    mock_response = mocker.Mock()
    mock_response.content = mock_naver_html.encode("euc-kr")
    mock_response.raise_for_status = mocker.Mock()

    mock_get = mocker.patch(
        "stock_analyzer.scrapers.company.naver_strategy.requests.get",
        return_value=mock_response,
    )

    return mock_get, mock_response


def test_naver_strategy_scrape_top_3(mock_requests_get_success):
    """상위 N 기업 이름을 파싱해 리스트로 반환한다."""

    strategy = NaverFinanceStrategy(top_n=3)

    top_companies = strategy.scrape()

    assert top_companies == ["가짜전자", "가짜하이닉스", "가짜에너지솔루션"]

    mock_get, _ = mock_requests_get_success
    mock_get.assert_called_once()


def test_naver_strategy_returns_empty_on_request_exception(mocker):
    """네트워크 예외 발생 시 빈 리스트를 반환한다."""

    mocker.patch(
        "stock_analyzer.scrapers.company.naver_strategy.requests.get",
        side_effect=requests.exceptions.RequestException("boom"),
    )

    strategy = NaverFinanceStrategy(top_n=5)

    assert strategy.scrape() == []