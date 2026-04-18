from datetime import datetime
from typing import Any, Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedDocumentTypeField"]


class SerializedDocumentTypeField(ConfiguredBaseModel):
    code: str
    name: str
    required: bool = False
    type: str = Field(..., alias="fieldType")
    document_type_id: Optional[str] = Field(None, alias="documentTypeCode")
    id: Optional[str] = Field(None, alias="pk")
    order: Optional[int] = 0
    field_data: Optional[dict[str, Any]] = Field(None, alias="fieldMeta")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    confidential: bool = Field(default=False, alias="confidential")
    read_only: bool = Field(default=False, alias="readOnly")
