from typing import TypedDict

__all__ = ["States", "Status"]


class Status(TypedDict):
    title: str
    name: str


States = dict[str, Status]
