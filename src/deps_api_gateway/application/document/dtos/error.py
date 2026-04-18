from typing import Optional, TypedDict

from ..state import DocumentState

__all__ = ["Error"]


class Error(TypedDict):
    description: str
    inState: Optional[DocumentState]
