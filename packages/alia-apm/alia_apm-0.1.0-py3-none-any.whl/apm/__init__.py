from typing import Any


def default(value: Any, default_value: Any) -> Any:
    return default_value if value is None else value
