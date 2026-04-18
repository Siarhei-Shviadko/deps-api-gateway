from enum import Enum

__all__ = ["ElementType"]


class ElementType(str, Enum):
    IMAGE = "image"
    POSITIONAL_TEXT = "positional_text"
    TABLE = "table"
