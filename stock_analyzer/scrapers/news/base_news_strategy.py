import sys
from pathlib import Path
from abc import ABC, abstractmethod

# 프로젝트 루트를 Python 경로에 추가 (직접 실행 시에만)
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(project_root))

from utils.logger import Logging

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

if __name__ == "__main__":
    # 추상 클래스이므로 직접 실행할 수 없습니다
    Logging.info("BaseNewsStrategy는 추상 클래스입니다.")
    Logging.info("google_news_strategy.py를 실행하거나 main.py를 사용하세요.")