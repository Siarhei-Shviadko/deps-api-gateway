from typing import Optional

from pydantic import Field

from deps_api_gateway.application.document import (
    ContainerTypes,
    DocumentAssignmentStatus,
    DocumentPriority,
    DocumentState,
)

from ...base import ConfiguredBaseModel
from .blob_file import SerializedBlobFile
from .comments import SerializedCommentsList
from .container_email_metadata import SerializedContainerEmailMetadata
from .error import SerializedError
from .group_info import SerializedGroupInfo
from .labels import SerializedLabel
from .relation import SerializedRelation
from .reviewer import SerializedReviewer

__all__ = ["SerializedDocument"]


class SerializedDocument(ConfiguredBaseModel):
    pk: Optional[str] = Field(alias="_id")
    parent_id: Optional[str] = Field(alias="parentId")

    title: str
    state: DocumentState
    files: list[SerializedBlobFile]
    document_type: Optional[str] = Field(alias="documentType")
    sub_type: Optional[str] = Field(alias="modelName")
    date: Optional[str]
    source_code: Optional[str] = Field(alias="source")
    reviewer: Optional[SerializedReviewer]
    labels: list[SerializedLabel] = Field(default_factory=list)
    group_id: Optional[str] = Field(alias="groupId", deprecated=True)
    group_info: Optional[SerializedGroupInfo] = Field(alias="groupInfo")
    language: Optional[str]
    engine: Optional[str]
    llm_type: Optional[str] = Field(None, alias="llmType")
    communication: Optional[SerializedCommentsList] = None
    preview_documents: Optional[dict[str, SerializedBlobFile]] = Field(alias="previewDocuments")
    processing_documents: Optional[dict[str, SerializedBlobFile]] = Field(alias="processingDocuments")
    error: Optional[SerializedError]
    container_type: Optional[ContainerTypes] = Field(alias="containerType")
    container_metadata: Optional[SerializedContainerEmailMetadata] = Field(alias="containerMetadata")
    assigned_relations: list[SerializedRelation] = Field(default_factory=list, alias="assignedRelations")
    assignment_status: Optional[DocumentAssignmentStatus] = Field(
        DocumentAssignmentStatus.UNASSIGNED, alias="assignmentStatus"
    )
    priority: Optional[DocumentPriority] = DocumentPriority.LOW
