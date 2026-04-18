from typing import Optional, TypedDict

from ..container_types import ContainerTypes
from ..state import DocumentState
from .blob_file import UpdateDocumentBlobFile
from .container_email_metadata import ContainerEmailMetadata
from .error import Error
from .reviewer import Reviewer

__all__ = ["PartialUpdateDocumentData"]


class PartialUpdateDocumentData(TypedDict, total=False):
    title: Optional[str]
    state: Optional[DocumentState]
    files: Optional[list[UpdateDocumentBlobFile]]
    documentType: Optional[str]
    subType: Optional[str]
    date: Optional[str]
    sourceCode: Optional[str]
    reviewer: Optional[Reviewer]
    language: Optional[str]
    engine: Optional[str]
    previewDocuments: Optional[dict[str, UpdateDocumentBlobFile]]
    processingDocuments: Optional[dict[str, UpdateDocumentBlobFile]]
    error: Optional[Error]
    containerType: Optional[ContainerTypes]
    containerMetadata: Optional[ContainerEmailMetadata]
