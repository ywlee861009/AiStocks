import pytest
import requests # Mock 객체로 대체될 예정
from bs4 import BeautifulSoup

# 우리가 테스트할 대상 (소스 코드)
from stock_analyzer.scrapers.naver_strategy import NaverFinanceStrategy

# --- 1. 가짜 데이터 준비 (Fixture) ---
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

# --- 2. Mock 객체 준비 (Fixture) ---
@pytest.fixture
def mock_requests_get(mocker, mock_naver_html):
    """
    requests.get() 함수를 흉내 냅니다.
    'mocker'는 pytest-mock 라이브러리가 제공하는 강력한 도구입니다.
    """
    
    # 1. 가짜 Response 객체를 만듭니다.
    #    (NaverFinanceStrategy가 response.content와 response.raise_for_status()를 쓰기 때문)
    mock_response = mocker.Mock()
    mock_response.content = mock_naver_html.encode('euc-kr') # 인코딩까지 흉내
    mock_response.raise_for_status = mocker.Mock() # 이 함수는 호출해도 아무 일도 없도록
    
    # 2. 'requests' 모듈의 'get' 함수를 'mock_response'를 반환하도록 대체합니다.
    #    [중요] 'stock_analyzer.scrapers.naver_strategy.requests'가 아닌,
    #    실제 import가 일어나는 'requests'를 모킹해야 하지만,
    #    naver_strategy.py가 'import requests'를 사용하므로 'requests.get'을 모킹합니다.
    #    (더 쉬운 방법: naver_strategy.py 내부의 _fetch_page를 모킹할 수도 있습니다)
    
    # 여기서는 'requests' 모듈 자체의 'get'을 모킹합니다.
    mock_get = mocker.patch("requests.get", return_value=mock_response)
    
    return mock_get, mock_response

# --- 3. 실제 테스트 함수 ---
def test_naver_strategy_scrape_top_3(mock_requests_get, mock_naver_html):
    """
    NaverFinanceStrategy가 상위 3개 기업을 잘 가져오는지 테스트합니다.
    (네트워크 접속 X)
    """
    # given: 상위 3개를 가져오는 전략 객체 생성
    strategy = NaverFinanceStrategy(top_n=3)
    
    # when: 스크래핑 실행
    top_companies = strategy.scrape()
    
    # then: 결과 검증
    # 1. 반환된 리스트의 길이가 3개인가?
    assert len(top_companies) == 3
    
    # 2. 첫 번째 결과가 '가짜전자'인가?
    assert top_companies[0] == "가짜전자"
    
    # 3. 마지막 결과가 '가짜에너지솔루션'인가?
    assert top_companies[2] == "가짜에너지솔루션"
    
    # 4. 'requests.get'이 실제로 1번 호출되었는지 검증 (추가 검증)
    mock_get, _ = mock_requests_get
    mock_get.assert_called_once()