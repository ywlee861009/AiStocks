from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseSaver(ABC):
    """데이터 저장을 위한 인터페이스(추상 클래스)."""

    @abstractmethod
    def save(self, data: Dict[str, Any], path: str) -> str:
        """데이터를 저장하고 저장된 파일 경로를 반환한다."""
        raise NotImplementedError