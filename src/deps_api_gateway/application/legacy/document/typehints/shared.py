from typing import TypedDict

__all__ = ["CodeName", "Label", "DocumentReviewer", "GenericRestResponse"]


class CodeName(TypedDict):
    code: str
    name: str


class Label(TypedDict):
    _id: str
    name: str


class DocumentReviewer(TypedDict):
    id: str
    email: str
    firstName: str
    lastName: str


class GenericRestResponse(TypedDict):
    code: int
    content: bytes  # noqa: WPS110
    headers: dict
