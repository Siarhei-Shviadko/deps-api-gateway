from typing import Any, Optional

from pydantic import Field

from deps_api_gateway.application.types import FieldType

from ...base import ConfiguredBaseModel

__all__ = ["SerializedField", "SerializedFields"]


class SerializedField(ConfiguredBaseModel):
    name: str
    code: str
    id: Optional[str] = Field(None, alias="pk")
    document_type_id: Optional[str] = Field(None, alias="documentTypeCode")
    required: bool = False
    order: Optional[int] = 0
    field_type: FieldType = Field(alias="fieldType")
    confidential: bool = Field(default=False, alias="confidential")
    read_only: bool = Field(default=False, alias="readOnly")
    field_data: Optional[dict[str, Any]] = Field(..., alias="fieldMeta")


class SerializedFields(ConfiguredBaseModel):
    fields: list[SerializedField]
