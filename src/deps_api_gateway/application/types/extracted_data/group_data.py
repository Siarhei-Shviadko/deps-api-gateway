from typing import TypedDict

__all__ = ["GroupData"]


class GroupData(TypedDict, total=False):
    order: int
    name: str
    elements: list[str]
