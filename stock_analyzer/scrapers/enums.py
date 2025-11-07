from enum import Enum, auto

class CompanyScrapeSource(Enum):
    """
    어디서 '기업 목록'을 스크래핑할지 정의하는 Enum
    """
    NAVER_FINANCE = auto()
    # DAUM_FINANCE = auto()

class NewsFetchSource(Enum):
    """
    어디서 '뉴스 피드'를 가져올지 정의하는 Enum
    """
    GOOGLE_NEWS_RSS = auto()