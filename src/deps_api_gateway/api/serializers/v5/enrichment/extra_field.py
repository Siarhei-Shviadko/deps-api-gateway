from enum import Enum
from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedExtraField", "ExtraFieldType", "SaveExtraFieldResponse", "UpdateExtraFieldsRequest"]


class ExtraFieldType(str, Enum):
    STRING = "string"


class SerializedExtraField(ConfiguredBaseModel):
    code: str
    name: str
    type: ExtraFieldType
    auto_filled: bool = Field(..., alias="autoFilled")


class SaveExtraFieldResponse(ConfiguredBaseModel):
    code: str


class UpdateExtraFieldRequest(ConfiguredBaseModel):
    code: str
    name: Optional[str]
    display_order: Optional[int] = Field(default=None, alias="order")


class UpdateExtraFieldsRequest(ConfiguredBaseModel):
    extra_fields: list[UpdateExtraFieldRequest] = Field(..., alias="extraFields")
