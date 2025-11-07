import sys
from datetime import datetime
from typing import Optional

class Logging:
    """
    커스텀 로거 클래스
    print 문을 대체하여 일관된 로깅 포맷을 제공합니다.
    """
    
    # 로그 레벨 상수
    INFO = "INFO"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    
    def __init__(self, name: Optional[str] = None):
        """
        Args:
            name: 로거 이름 (기본값: None)
        """
        self.name = name
    
    def _format_message(self, level: str, message: str) -> str:
        """로그 메시지 포맷팅"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.name:
            return f"[{timestamp}] [{level}] [{self.name}] {message}"
        return f"[{timestamp}] [{level}] {message}"
    
    def info(self, message: str):
        """정보 로그 출력"""
        formatted = self._format_message(self.INFO, message)
        print(formatted, file=sys.stdout)
    
    def error(self, message: str):
        """에러 로그 출력"""
        formatted = self._format_message(self.ERROR, message)
        print(formatted, file=sys.stderr)
    
    def success(self, message: str):
        """성공 로그 출력"""
        formatted = self._format_message(self.SUCCESS, message)
        print(formatted, file=sys.stdout)
    
    def warning(self, message: str):
        """경고 로그 출력"""
        formatted = self._format_message(self.WARNING, message)
        print(formatted, file=sys.stderr)
    
    def __call__(self, message: str, level: str = INFO):
        """직접 호출 시 info 레벨로 출력"""
        if level == self.INFO:
            self.info(message)
        elif level == self.ERROR:
            self.error(message)
        elif level == self.SUCCESS:
            self.success(message)
        elif level == self.WARNING:
            self.warning(message)
        else:
            self.info(message)

