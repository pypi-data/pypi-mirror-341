from typing import Any


def required(field: Any) -> str:
    if not field:
        raise ValueError("Field is required")
    return field
