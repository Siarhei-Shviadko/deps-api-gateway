from enum import Enum

__all__ = ["Provider"]


class Provider(str, Enum):
    LLAMAINDEX = "llamaindex"
