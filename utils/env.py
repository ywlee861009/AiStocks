import os

from utils.logger import Logging


def get_env_int(var_name: str, default: int, *, aliases: tuple[str, ...] = ()) -> int:
    """환경 변수(및 대체 이름)에서 정수 값을 안전하게 읽어옵니다."""
    candidate_names = (var_name, *aliases)

    for name in candidate_names:
        value = os.environ.get(name)
        if value is None:
            continue

        try:
            parsed_value = int(value)
            if parsed_value <= 0:
                Logging.warning(
                    f"환경 변수 '{name}' 값이 양의 정수가 아닙니다: {value!r}. 기본값 {default} 사용"
                )
                return default

            if name != var_name:
                Logging.info(
                    f"환경 변수 '{name}' 값을 사용합니다. (우선순위: '{var_name}' -> {aliases})"
                )
            return parsed_value
        except (TypeError, ValueError):
            Logging.warning(
                f"환경 변수 '{name}' 값이 정수가 아닙니다: {value!r}. 기본값 {default} 사용"
            )
            return default

    return default

