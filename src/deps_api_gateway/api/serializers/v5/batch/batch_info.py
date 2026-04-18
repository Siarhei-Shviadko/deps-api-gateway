from datetime import datetime
from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedBatchInfo"]


class SerializedFileInfo(ConfiguredBaseModel):
    id: str
    name: str
    status: str
    document_type_id: Optional[str] = Field(default=None, alias="documentTypeId")
    engine: Optional[str]
    llm_type: Optional[str] = Field(default=None, alias="llmType")
    parsing_features: Optional[list[str]] = Field(default=None, alias="parsingFeatures")


class SerializedBatchInfo(ConfiguredBaseModel):
    id: str
    name: str
    status: str
    group: Optional[str]
    created_at: datetime = Field(..., alias="createdAt")
    files: list[SerializedFileInfo]
