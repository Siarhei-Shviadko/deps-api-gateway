from typing import TypedDict

__all__ = ["Bbox"]


class Bbox(TypedDict):
    x: float
    y: float
    w: float
    h: float
