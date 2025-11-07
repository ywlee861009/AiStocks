import requests
from bs4 import BeautifulSoup
from .base_strategy import BaseScraperStrategy  # <-- [중요] 상대 경로로 변경

class NaverFinanceStrategy(BaseScraperStrategy):
    """
    '네이버 금융'에서 KOSPI 시총 순위를 가져오는 실제 전략 클래스
    """
    BASE_URL = "https://finance.naver.com/sise/sise_market_sum.naver"

    def _fetch_page(self):
        try:
            response = requests.get(self.BASE_URL, headers=self.HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='euc-kr')
            return soup
        except requests.exceptions.RequestException as e:
            self.logging.error(f"웹페이지를 가져오는 데 실패했습니다 - {e}")
            return None

    def scrape(self):
        self.logging.info(f"상위 {self.top_n}개 기업 스크래핑 시작...")
        soup = self._fetch_page()
        if soup is None:
            return []

        company_list = []
        try:
            company_tags = soup.select("table.type_2 tbody tr td a.tltle")
            for tag in company_tags:
                company_name = tag.text.strip()
                if company_name:
                    company_list.append(company_name)
                if len(company_list) == self.top_n:
                    break
            
            self.logging.success(f"{len(company_list)}개 기업 목록을 가져왔습니다.")
            return company_list
        except Exception as e:
            self.logging.error(f"데이터 파싱 중 문제가 발생했습니다 - {e}")
            return []