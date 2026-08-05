from enum import Enum

__all__ = ["GetGroupExtras", "GetGroupsExtras"]


class GetGroupExtras(str, Enum):
    CLASSIFIERS = "classifiers"
    SPLITTERS = "splitters"


class GetGroupsExtras(str, Enum):
    SPLITTERS = "splitters"
