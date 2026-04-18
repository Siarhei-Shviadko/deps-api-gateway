from typing import List, Optional, TypedDict

from .shared import DocumentReviewer, Label

__all__ = ["DocumentListProxyResponse", "Document"]


class File(TypedDict):
    blobName: str
    url: str


class Communication(TypedDict):
    comments: List[str]


class Document(TypedDict):
    _id: str
    parentId: str
    title: str
    state: str
    files: List[File]
    documentType: str
    modelName: str
    date: str
    source: str
    reviewer: Optional[DocumentReviewer]
    labels: List[Label]
    language: str
    engine: str
    communication: Communication
    previewDocuments: dict[str, File]
    processingDocuments: dict[str, File]
    error: str
    containerType: str
    containerMetadata: str
    assignedRelations: List[str]
    assignmentStatus: str
    priority: str


class DocumentListMeta(TypedDict):
    total: int
    size: int


class DocumentListProxyResponse(TypedDict):
    meta: DocumentListMeta
    result: List[Document]  # noqa: WPS110
