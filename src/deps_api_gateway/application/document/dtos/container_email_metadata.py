from typing import Optional, TypedDict

__all__ = ["ContainerEmailMetadata"]


class ContainerEmailMetadata(TypedDict):
    firstLevelChildCount: Optional[int]
    subject: Optional[str]
    sender: Optional[str]
    recipients: Optional[list[str]]
    cc: Optional[list[str]]
    body: Optional[str]
    date: Optional[str]
