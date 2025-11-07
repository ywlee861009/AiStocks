import requests
from bs4 import BeautifulSoup
import os                  # .env 파일을 읽기 위해 import
from dotenv import load_dotenv  # .env 파일을 읽기 위해 import

class NaverFinanceScraper:
    """
    네이버 금융에서 KOSPI 시가총액 기준 상위 N개 기업을 스크래핑하는 클래스
    """
    
    # 공통으로 사용할 URL과 헤더를 클래스 변수로 선언
    BASE_URL = "https://finance.naver.com/sise/sise_market_sum.naver"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def __init__(self, top_n=10):
        """
        스크래퍼 객체를 초기화합니다.
        
        :param top_n: 가져올 기업의 수 (기본값 10)
        """
        try:
            # top_n을 정수형으로 변환하여 저장
            self.top_n = int(top_n)
        except ValueError:
            print(f"경고: top_n 값({top_n})이 유효하지 않아 기본값(10)을 사용합니다.")
            self.top_n = 10
            
        print(f"[Scraper] 초기화 완료: 상위 {self.top_n}개 기업을 대상으로 합니다.")

    def _fetch_page(self):
        """
        [Private] 네이버 금융 페이지에 요청을 보내고 HTML을 파싱합니다.
        성공 시 BeautifulSoup 객체를, 실패 시 None을 반환합니다.
        """
        try:
            response = requests.get(self.BASE_URL, headers=self.HEADERS)
            response.raise_for_status()  # 200 OK가 아니면 오류 발생
            
            # 네이버 금융은 'euc-kr' 인코딩을 사용
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='euc-kr')
            return soup
        
        except requests.exceptions.RequestException as e:
            print(f"오류: 웹페이지를 가져오는 데 실패했습니다 - {e}")
            return None

    def get_top_companies(self):
        """
        시가총액 상위 N개 기업 목록을 스크래핑하여 리스트로 반환합니다.
        
        :return: 기업명 리스트 (예: ['삼성전자', 'SK하이닉스', ...])
        """
        print(f"[Scraper] 상위 {self.top_n}개 기업 스크래핑을 시작합니다...")
        
        soup = self._fetch_page()
        if soup is None:
            return []  # 페이지 로딩 실패 시 빈 리스트 반환

        company_list = []
        
        try:
            # 목표 테이블: "table.type_2" 안의 "a.tltle" 태그
            company_tags = soup.select("table.type_2 tbody tr td a.tltle")

            for tag in company_tags:
                company_name = tag.text.strip()
                
                # .strip() 후 빈 문자열이 아닌지 확인
                if company_name:
                    company_list.append(company_name)
                
                # N개가 채워지면 즉시 중단
                if len(company_list) == self.top_n:
                    break
            
            if not company_list:
                print("오류: 기업 목록을 찾지 못했습니다. (웹페이지 구조 변경 가능성)")
            else:
                print(f"[Scraper] 성공: {len(company_list)}개 기업 목록을 가져왔습니다.")

            return company_list
        
        except Exception as e:
            print(f"오류: 데이터 파싱 중 문제가 발생했습니다 - {e}")
            return []

# --- 이 스크립트를 직접 실행했을 때만 아래 코드가 동작 ---
if __name__ == "__main__":
    
    # 1. .env 파일에서 환경 변수 로드
    load_dotenv()
    
    # 2. 'TOP_N' 환경 변수 읽기 (값이 없으면 기본값 '10' 사용)
    COMPANY_COUNT = os.environ.get('TOP_N', 10)
    
    # 3. 설정값(N)을 바탕으로 스크래퍼 객체 생성
    scraper = NaverFinanceScraper(top_n=COMPANY_COUNT)
    
    # 4. 스크래핑 실행
    top_companies = scraper.get_top_companies()
    
    if top_companies:
        print(f"\n---  KOSPI 시가총액 TOP {len(top_companies)} ---")
        for index, company in enumerate(top_companies, 1):
            print(f"{index}. {company}")