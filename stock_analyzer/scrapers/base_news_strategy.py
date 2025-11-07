from abc import ABC, abstractmethod
from stock_analyzer.logger import Logging

class BaseNewsStrategy(ABC):
    """
    모든 뉴스 패치 '전략'들이 반드시 따라야 하는 뼈대
    """
    def __init__(self, query_limit=20):
        self.query_limit = query_limit
        Logging.info(f"준비 완료: 최대 {self.query_limit}개 뉴스 대상", name=self.__class__.__name__)

    @abstractmethod
    def fetch_news(self, company_name: str):
        """
        지정된 회사의 뉴스 피드를 가져옵니다.
        :param company_name: 검색할 기업명 (예: '삼성전자')
        :return: 뉴스 항목 딕셔너리의 리스트 (예: [{'title': ..., 'link': ...}, ...])
        """
        pass