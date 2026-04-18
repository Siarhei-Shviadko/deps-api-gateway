from typing import List, TypedDict

__all__ = ["DocumentTypeResponse"]


class Field(TypedDict):
    name: str
    required: bool
    order: int
    fieldType: str
    fieldMeta: str
    pk: str
    code: str
    documentTypeCode: str


class DocumentTypeResponse(TypedDict):
    id: str
    created_at: str
    tenantId: str
    documentType: str
    extractionType: str
    fields: List[Field]
    engine: str
    language: str
    description: str
