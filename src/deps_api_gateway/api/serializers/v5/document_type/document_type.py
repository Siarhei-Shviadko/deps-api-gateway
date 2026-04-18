from datetime import datetime
from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from ..workflow_manager import SerializedWorkflowConfiguration

__all__ = [
    "SerializedDocumentType",
    "DocumentTypesResponse",
    "UpdateDocumentTypeLLMRequest",
    "UpdateDocumentTypeLLMResponse",
]


class SerializedDocumentType(ConfiguredBaseModel):
    id: str
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    tenant_id: str = Field(alias="tenantId")
    document_type: str = Field(alias="documentType")
    extraction_type: Optional[str] = Field(None, alias="extractionType")
    engine: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    llm_type: Optional[str] = Field(None, alias="llmType")
    workflow_configuration: Optional[SerializedWorkflowConfiguration] = Field(None, alias="workflowConfiguration")


class DocumentTypesResponse(ConfiguredBaseModel):
    result: list[SerializedDocumentType]


class UpdateDocumentTypeLLMRequest(ConfiguredBaseModel):
    llm_type: str = Field(alias="llmType", min_length=3, max_length=100)


class UpdateDocumentTypeLLMResponse(ConfiguredBaseModel):
    document_type_id: str = Field(alias="documentTypeId")
    llm_type: str = Field(alias="llmType")
