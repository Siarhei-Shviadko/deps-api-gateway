from typing import Any, List, Optional, TypedDict, Union

from .shared import CodeName, DocumentReviewer

__all__ = ["AggregatedDocumentList", "TaskResult", "AggregatedDocument", "ResponseLabel"]

TaskResult = Union[Any, BaseException]


class ResponseLabel(TypedDict):
    id: str
    name: str


class AggregatedDocument(TypedDict):
    id: str
    title: str
    date: str
    documentType: Optional[CodeName]
    state: Optional[CodeName]
    engine: Optional[CodeName]
    labels: List[ResponseLabel]
    reviewer: Optional[DocumentReviewer]
    language: Optional[CodeName]


class AggregatedDocumentList(TypedDict):
    total: int
    size: int
    result: List[AggregatedDocument]  # noqa:WPS110
