from typing import Optional

from pydantic import Field

from deps_api_gateway.application.document import (
    ContainerTypes,
    DocumentState,
    PartialUpdateDocumentData,
)

from ...base import ConfiguredBaseModel
from .blob_file import UpdateDocumentBlobFileData
from .container_email_metadata import SerializedContainerEmailMetadata
from .error import SerializedError
from .reviewer import SerializedReviewer

__all__ = ["PartialUpdateDocumentRequest"]


class PartialUpdateDocumentRequest(ConfiguredBaseModel):
    title: Optional[str] = None
    state: Optional[DocumentState] = None
    files: Optional[list[UpdateDocumentBlobFileData]] = Field(default_factory=list)
    document_type: Optional[str] = Field(default=None, alias="documentType")
    sub_type: Optional[str] = Field(default=None, alias="modelName")
    date: Optional[str] = None
    source_code: Optional[str] = Field(default=None, alias="source")
    reviewer: Optional[SerializedReviewer] = None
    language: Optional[str] = None
    engine: Optional[str] = None
    preview_documents: Optional[dict[str, UpdateDocumentBlobFileData]] = Field(
        default=None,
        alias="previewDocuments",
        description="Keys must be strings containing integers",
    )
    processing_documents: Optional[dict[str, UpdateDocumentBlobFileData]] = Field(
        default=None,
        alias="processingDocuments",
        description="Keys must be strings containing integers",
    )
    error: Optional[SerializedError] = None
    container_type: Optional[ContainerTypes] = Field(default=None, alias="containerType")
    container_metadata: Optional[SerializedContainerEmailMetadata] = Field(default=None, alias="containerMetadata")

    def to_dto(self) -> PartialUpdateDocumentData:
        return PartialUpdateDocumentData(**self.model_dump(by_alias=True, exclude_unset=True))
