from enum import Enum

__all__ = ["DocumentPriority"]


class DocumentPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
