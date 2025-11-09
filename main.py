import os
from dotenv import load_dotenv
import json

from typing import Optional
from savers.base_saver import BaseSaver
from savers.file_saver import FileSaver
from stock_analyzer.scrapers.enums import CompanyScrapeSource, NewsFetchSource
from stock_analyzer.scrapers.company.company_scraper import TopCompaniesScraper
from stock_analyzer.scrapers.news.news_fetcher import NewsFetcher
from stock_analyzer.logger import Logging
from stock_analyzer.utils.env import get_env_int

def run_step1():
    """1단계: Top N 기업 목록 가져오기"""
    Logging.info("--- 1단계: Top N 기업 목록 스크래핑 시작 ---")
    load_dotenv()
    COMPANY_COUNT = get_env_int('TOP_COMPANIES_COUNT', 10, aliases=('TOP_N',))
    
    scraper = TopCompaniesScraper(top_n=COMPANY_COUNT)
    
    try:
        # [수정] Enum 이름 변경ㅔ
        top_companies = scraper.get_top_companies(CompanyScrapeSource.NAVER_FINANCE) 
        
        if top_companies:
            Logging.success(f"KOSPI TOP {len(top_companies)} (Source: NAVER)")
            for index, company in enumerate(top_companies, 1):
                Logging.info(f"{index}. {company}")
            Logging.info("----------------------------------------")
            return top_companies
        else:
            Logging.error("스크래핑 실패")
            Logging.info("----------------------------------------")
            return []
    except ValueError as e:
        Logging.error(str(e))
        return []

def run_step2(company_list: list):
    """2단계: 기업별 뉴스 RSS 피드 가져오기"""
    Logging.info("--- 2단계: 기업별 뉴스 RSS 피드 가져오기 시작 ---")
    if not company_list:
        Logging.warning("기업 목록이 없어 2단계를 건너뜁니다.")
        Logging.info("----------------------------------------")
        return {} # 빈 딕셔너리 반환

    # .env에서 뉴스 개수(N)를 가져올 수도 있습니다.
    NEWS_COUNT_PER_COMPANY = get_env_int('NEWS_N', 20) # 20개
    
    fetcher = NewsFetcher(limit_per_company=NEWS_COUNT_PER_COMPANY)
    
    all_news_results = {}
    
    # 1단계에서 받은 기업 리스트를 순회
    for company in company_list:
        news_list = fetcher.get_news(company, NewsFetchSource.GOOGLE_NEWS_RSS)
        all_news_results[company] = news_list # {'삼성전자': [...뉴스 리스트...], ...}
    
    Logging.success("모든 기업의 뉴스 수집 완료.")
    Logging.info("----------------------------------------")
    return all_news_results

def run_step3(all_news_data: dict, output_path: str = "data.json", saver: Optional[BaseSaver] = None) -> str:
    """3단계: 수집된 데이터를 저장. saver가 주어지지 않으면 FileSaver 사용."""
    Logging.info("--- 3단계: 수집된 데이터를 저장합니다 ---")
    if not all_news_data:
        Logging.warning("저장할 데이터가 없습니다.")
        return ""
    saver = saver or FileSaver()
    saved_path = saver.save(all_news_data, output_path)
    Logging.success(f"데이터가 저장되었습니다: {saved_path}")
    Logging.info("----------------------------------------")
    return saved_path

# --- 이 스크립트를 직접 실행했을 때만 아래 코드가 동작 ---
if __name__ == "__main__":
    
    # 1단계 실행
    top_companies_list = run_step1()
    
    # 2단계 실행
    all_news_data = run_step2(top_companies_list)
    
    # 2단계 최종 결과 요약 출력
    if all_news_data:
        Logging.info("[최종 요약 (2단계 완료)]")
        for company, news_list in all_news_data.items():
            Logging.info(f"  > '{company}': {len(news_list)}개 뉴스 수집 완료")
            
        # 3단계를 위해 전체 결과를 JSON으로 간단히 출력해보기
        # (json.dumps는 딕셔너리를 예쁜 문자열로 만들어줍니다)
        Logging.info("[3단계로 넘어갈 데이터 샘플 (첫 번째 기업)]")
        if top_companies_list:
            first_company = top_companies_list[0]
            Logging.info(json.dumps(all_news_data[first_company][:2], indent=2, ensure_ascii=False))

    # 새로 추가된 3단계: 파일로 저장 (기본 경로: data.json)
    run_step3(all_news_data, output_path="data.json")