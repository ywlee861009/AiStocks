import sys
from datetime import datetime
from typing import Optional

class Logging:
    """
    커스텀 로거 클래스
    print 문을 대체하여 일관된 로깅 포맷을 제공합니다.
    
    사용 방법 (정적 메서드):
        Logging.info("message")
        Logging.info("message", name="CustomName")
        Logging.error("error message")
        Logging.success("success message")
        Logging.warning("warning message")
    """
    
    # 로그 레벨 상수
    INFO = "INFO"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    
    @staticmethod
    def _format_message(level: str, message: str, name: Optional[str] = None) -> str:
        """로그 메시지 포맷팅"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if name:
            return f"[{timestamp}] [{level}] [{name}] {message}"
        return f"[{timestamp}] [{level}] {message}"
    
    @staticmethod
    def info(message: str, name: Optional[str] = None):
        """정보 로그 출력 - Logging.info("message") 형태로 사용"""
        formatted = Logging._format_message(Logging.INFO, message, name)
        print(formatted, file=sys.stdout)
    
    @staticmethod
    def error(message: str, name: Optional[str] = None):
        """에러 로그 출력 - Logging.error("message") 형태로 사용"""
        formatted = Logging._format_message(Logging.ERROR, message, name)
        print(formatted, file=sys.stderr)
    
    @staticmethod
    def success(message: str, name: Optional[str] = None):
        """성공 로그 출력 - Logging.success("message") 형태로 사용"""
        formatted = Logging._format_message(Logging.SUCCESS, message, name)
        print(formatted, file=sys.stdout)
    
    @staticmethod
    def warning(message: str, name: Optional[str] = None):
        """경고 로그 출력 - Logging.warning("message") 형태로 사용"""
        formatted = Logging._format_message(Logging.WARNING, message, name)
        print(formatted, file=sys.stderr)
