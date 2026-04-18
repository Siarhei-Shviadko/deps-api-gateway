from enum import Enum

__all__ = ["Format"]


class Format(str, Enum):
    EXCEL = "excel"
    JSON = "json"
