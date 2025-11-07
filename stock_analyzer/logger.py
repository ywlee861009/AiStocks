import sys
from datetime import datetime
from typing import Optional

class _LogMethod:
    """인스턴스와 정적 모두 지원하는 로그 메서드 descriptor"""
    def __init__(self, level: str, is_error: bool = False):
        self.level = level
        self.is_error = is_error
    
    def __get__(self, instance, owner):
        if instance is None:
            # 클래스에서 호출된 경우 (정적 메서드처럼)
            def static_method(message: str, name: Optional[str] = None):
                formatted = Logging._format_message(self.level, message, name)
                print(formatted, file=sys.stderr if self.is_error else sys.stdout)
            return static_method
        else:
            # 인스턴스에서 호출된 경우
            def instance_method(message: str):
                formatted = instance._format_message(self.level, message, instance.name)
                print(formatted, file=sys.stderr if self.is_error else sys.stdout)
            return instance_method


class Logging:
    """
    커스텀 로거 클래스
    print 문을 대체하여 일관된 로깅 포맷을 제공합니다.
    
    사용 방법:
        1. 정적 방식 (Java의 static처럼): 
           Logging.info("message")
           Logging.info("message", name="CustomName")
        
        2. 인스턴스 방식:
           logger = Logging("LoggerName")
           logger.info("message")
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
    
    @staticmethod
    def _format_message(level: str, message: str, name: Optional[str] = None) -> str:
        """로그 메시지 포맷팅"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if name:
            return f"[{timestamp}] [{level}] [{name}] {message}"
        return f"[{timestamp}] [{level}] {message}"
    
    # Descriptor를 사용하여 인스턴스/정적 모두 지원
    info = _LogMethod(INFO, is_error=False)
    success = _LogMethod(SUCCESS, is_error=False)
    error = _LogMethod(ERROR, is_error=True)
    warning = _LogMethod(WARNING, is_error=True)
    
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
