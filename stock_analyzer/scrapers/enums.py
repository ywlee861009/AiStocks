from enum import Enum, auto

class ScrapeSource(Enum):
    """
    어디서 스크래핑을 수행할지 정의하는 Enum
    """
    NAVER_FINANCE = auto()
    # DAUM_FINANCE = auto()