import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가 (직접 실행 시에만)
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(project_root))

import feedparser
from urllib.parse import quote_plus  # 기업명(한글)을 URL 인코딩하기 위해

# 직접 실행 vs 모듈로 import 구분
if __name__ == "__main__":
    from stock_analyzer.scrapers.news.base_news_strategy import BaseNewsStrategy
else:
    from .base_news_strategy import BaseNewsStrategy

from utils.logger import Logging

class GoogleNewsRssStrategy(BaseNewsStrategy):
    """
    '구글 뉴스' RSS 피드를 통해 뉴스를 가져오는 실제 전략 클래스
    """
    BASE_URL = "https://news.google.com/rss/search?hl=ko&gl=KR&ceid=KR:ko&q="

    def fetch_news(self, company_name: str):
        Logging.info(f"'{company_name}' 뉴스 검색 (RSS)...", name=self.__class__.__name__)

        # 1. 기업명을 URL에 맞게 인코딩 (예: '삼성전자' -> '%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90')
        encoded_company = quote_plus(company_name)
        feed_url = self.BASE_URL + encoded_company

        news_list = []
        try:
            # 2. feedparser로 RSS 피드를 파싱
            feed = feedparser.parse(feed_url)

            # 3. 각 뉴스 항목(entry)을 순회
            for entry in feed.entries:
                news_item = {
                    "title": entry.title,
                    "link": entry.link,
                    # 'published_parsed'는 파싱된 시간 객체, 'published'는 문자열
                    "pub_date": entry.get("published", "N/A"),
                    "source": entry.source.title if hasattr(entry, 'source') and entry.source else 'N/A'
                }
                news_list.append(news_item)

                # 4. 우리가 정한 N개 (query_limit) 만큼만 가져오고 중단
                if len(news_list) >= self.query_limit:
                    break

            Logging.success(f"'{company_name}' 뉴스 {len(news_list)}개 발견.", name=self.__class__.__name__)
            return news_list

        except Exception as e:
            Logging.error(f"{company_name} 뉴스 파싱 중 - {e}", name=self.__class__.__name__)
            return []

if __name__ == "__main__":
    # 테스트 실행
    Logging.info("GoogleNewsRssStrategy 테스트 실행 중...")
    strategy = GoogleNewsRssStrategy(query_limit=5)
    news = strategy.fetch_news("삼성전자")

    if news:
        Logging.success(f"'{news[0].get('source', 'N/A')}' 등 {len(news)}개 뉴스 발견")
        for idx, item in enumerate(news, 1):
            Logging.info(f"{idx}. {item['title']}")
    else:
        Logging.error("뉴스 가져오기 실패")