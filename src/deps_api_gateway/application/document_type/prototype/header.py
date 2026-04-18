from enum import Enum
from typing import TypedDict

__all__ = ["HeaderType", "Header"]


class HeaderType(str, Enum):
    ROWS = "rows"
    COLUMNS = "columns"


class Header(TypedDict):
    name: str
    aliases: list[str]
