from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

__all__ = ["ProfileData"]


class Format(str, Enum):
    EXCEL = "excel"
    JSON = "json"


@dataclass
class ProfileData:
    name: str
    schema: dict[str, Any]
    format: Optional[Format] = None
    external_storages_info: Optional[list[dict[str, Any]]] = None
