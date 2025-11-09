# ...existing code...
import json
from typing import Any, Dict
from .base_saver import BaseSaver

class FileSaver(BaseSaver):
    """JSON 파일로 저장하는 구현체."""

    def save(self, data: Dict[str, Any], path: str = "data.json") -> str:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path