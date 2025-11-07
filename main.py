import os
from dotenv import load_dotenv

# [중요] 우리가 만든 패키지에서 클래스들을 import 합니다.
from stock_analyzer.scrapers.company_scraper import TopCompaniesScraper
from stock_analyzer.scrapers.enums import ScrapeSource

def run_step1():
    """
    1단계: Top N 기업 목록 가져오기 실행
    """
    print("--- 1단계: Top N 기업 목록 스크래핑 시작 ---")
    
    # 1. .env 파일에서 환경 변수 로드
    load_dotenv()
    
    # 2. 'TOP_N' 환경 변수 읽기 (값이 없으면 기본값 '10' 사용)
    COMPANY_COUNT = os.environ.get('TOP_N', 10)
    
    # 3. 메인 스크래퍼 객체 생성
    scraper = TopCompaniesScraper(top_n=COMPANY_COUNT)
    
    # 4. 스크래핑 실행 (네이버 금융 소스)
    try:
        top_companies = scraper.get_top_companies(ScrapeSource.NAVER_FINANCE)
        
        if top_companies:
            print(f"\n[결과] KOSPI 시가총액 TOP {len(top_companies)} (Source: NAVER)")
            for index, company in enumerate(top_companies, 1):
                print(f"{index}. {company}")
            print("----------------------------------------")
            return top_companies # 2단계를 위해 결과를 반환합니다.
        else:
            print("[결과] 스크래핑에 실패했거나 데이터가 없습니다.")
            print("----------------------------------------")
            return []

    except ValueError as e:
        print(e)
        return []

# --- 이 스크립트를 직접 실행했을 때만 아래 코드가 동작 ---
if __name__ == "__main__":
    run_step1()