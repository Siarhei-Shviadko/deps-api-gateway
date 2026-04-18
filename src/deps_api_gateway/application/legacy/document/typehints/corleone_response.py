from typing import List, TypedDict

__all__ = ["CorleoneResponse"]


class Field(TypedDict):
    name: str
    required: bool
    order: int
    fieldType: str
    fieldMeta: dict
    pk: str
    code: str
    documentTypeCode: str


class DocType(TypedDict):
    pk: str
    code: str
    name: str
    engine: str
    language: str
    fields: List[Field]
    extractionType: str
    inProgress: bool


class Meta(TypedDict):
    total: int
    size: int


class CorleoneResponse(TypedDict):
    result: List[DocType]  # noqa: WPS110
    meta: Meta
