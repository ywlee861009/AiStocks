from ..enums import NewsFetchSource
from .google_news_strategy import GoogleNewsRssStrategy
from stock_analyzer.logger import Logging
# 나중에 네이버 뉴스 RSS 전략 등을 추가할 수 있습니다.

class NewsFetcher:
    """
    뉴스 패치 전략을 선택하고 실행하는 메인 컨트롤 타워 클래스
    """
    def __init__(self, limit_per_company=20):
        self.limit = limit_per_company
        
        self._strategies = {
            NewsFetchSource.GOOGLE_NEWS_RSS: GoogleNewsRssStrategy
        }
        Logging.info(f"초기화 완료: 기업별 뉴스 {self.limit}개 대상", name=self.__class__.__name__)

    def get_news(self, company_name: str, source: NewsFetchSource):
        if source not in self._strategies:
            raise ValueError(f"지원하지 않는 뉴스 소스입니다: {source}")

        StrategyClass = self._strategies[source]
        # 전략 객체 생성 시 쿼리 한도(limit)를 전달
        strategy_instance = StrategyClass(self.limit)
        
        return strategy_instance.fetch_news(company_name)