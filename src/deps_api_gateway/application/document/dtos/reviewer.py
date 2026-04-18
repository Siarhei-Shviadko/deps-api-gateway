from typing import Optional, TypedDict

__all__ = ["Reviewer"]


class Reviewer(TypedDict):
    id: str
    email: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
