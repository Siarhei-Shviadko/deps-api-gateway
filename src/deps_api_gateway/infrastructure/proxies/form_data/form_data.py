from dataclasses import dataclass
from typing import Any

__all__ = ["FormData"]


@dataclass
class FormData:
    headers: dict[str, Any]
    data: bytes
