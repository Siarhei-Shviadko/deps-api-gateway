from datetime import datetime
from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["WorkflowParams", "ProcessingParams", "SerializedFileInfo"]


class WorkflowParams(ConfiguredBaseModel):
    document_type_id: Optional[str] = Field(None, alias="documentTypeId")


class ProcessingParams(ConfiguredBaseModel):
    group_id: Optional[str] = Field(None, alias="groupId")
    splitting_enabled: bool = Field(..., alias="splittingEnabled")
    classification_enabled: bool = Field(..., alias="classificationEnabled")
    workflow_params: WorkflowParams = Field(..., alias="workflowParams")


class State(ConfiguredBaseModel):
    status: str
    error_message: Optional[str] = Field(None, alias="errorMessage")


class SerializedFileInfo(ConfiguredBaseModel):
    id: str
    tenant_id: str = Field(..., alias="tenantId")
    name: str
    path: str
    labels: Optional[list[str]] = None
    state: State
    processing_params: ProcessingParams = Field(..., alias="processingParams")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(..., alias="updatedAt")
