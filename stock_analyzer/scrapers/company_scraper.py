from .enums import CompanyScrapeSource
from .naver_strategy import NaverFinanceStrategy
from stock_analyzer.logger import Logging
# from .daum_strategy import DaumFinanceStrategy # 나중에 추가할 위치

class TopCompaniesScraper:
    """
    스크래핑 전략을 선택하고 실행하는 메인 컨트롤 타워 클래스
    """
    def __init__(self, top_n):
        self.top_n = top_n
        
        self._strategies = {
            CompanyScrapeSource.NAVER_FINANCE: NaverFinanceStrategy
            # ScrapeSource.DAUM_FINANCE: DaumFinanceStrategy
        }
        Logging.info(f"초기화 완료: 상위 {self.top_n}개 대상", name=self.__class__.__name__)

    def get_top_companies(self, source: CompanyScrapeSource):
        if source not in self._strategies:
            raise ValueError(f"지원하지 않는 소스입니다: {source}")

        StrategyClass = self._strategies[source]
        strategy_instance = StrategyClass(self.top_n)
        return strategy_instance.scrape()