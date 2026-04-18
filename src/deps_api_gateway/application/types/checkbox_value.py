from enum import Enum

__all__ = ["CheckboxValue"]


class CheckboxValue(str, Enum):
    CHECKED = "checked"
    UNCHECKED = "unchecked"
    UNRECOGNIZED = "unrecognized"
