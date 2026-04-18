from enum import Enum

__all__ = ["Severity"]


class Severity(str, Enum):
    WARNING = "warning"
    ERROR = "error"
