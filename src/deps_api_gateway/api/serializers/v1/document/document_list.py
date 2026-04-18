from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["AggregatedDocumentList"]


class DocumentLabel(ConfiguredBaseModel):
    id: str
    name: str


class DocumentReviewer(ConfiguredBaseModel):
    id: str
    email: str
    first_name: str
    last_name: str


class CodeName(ConfiguredBaseModel):
    code: str
    name: str


class AggregatedDocument(ConfiguredBaseModel):
    id: str
    title: str
    date: str
    document_type: Optional[CodeName]
    state: Optional[CodeName]
    engine: Optional[CodeName]
    labels: list[DocumentLabel] = Field(default_factory=list)
    reviewer: Optional[DocumentReviewer]
    language: Optional[CodeName]


class AggregatedDocumentList(ConfiguredBaseModel):
    total: int
    size: int
    result: list[AggregatedDocument]  # noqa: WPS411, WPS110
