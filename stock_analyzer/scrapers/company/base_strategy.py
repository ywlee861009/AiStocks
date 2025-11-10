import sys
from pathlib import Path
from abc import ABC, abstractmethod

# 프로젝트 루트를 Python 경로에 추가 (직접 실행 시에만)
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(project_root))

from utils.logger import Logging

class BaseScraperStrategy(ABC):
    """
    모든 스크래핑 '전략'들이 반드시 따라야 하는 뼈대(추상 클래스)
    """
    def __init__(self, top_n):
        self.top_n = top_n
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        Logging.info(f"준비 완료: 상위 {self.top_n}개 대상", name=self.__class__.__name__)

    @abstractmethod
    def scrape(self):
        """
        상위 N개 기업 목록을 스크래핑하여 리스트로 반환합니다.
        이 메소드는 하위 클래스에서 반드시 재정의(구현)해야 합니다.
        """
        pass

if __name__ == "__main__":
    # 추상 클래스이므로 직접 실행할 수 없습니다
    Logging.info("BaseScraperStrategy는 추상 클래스입니다.")
    Logging.info("naver_strategy.py를 실행하거나 main.py를 사용하세요.")