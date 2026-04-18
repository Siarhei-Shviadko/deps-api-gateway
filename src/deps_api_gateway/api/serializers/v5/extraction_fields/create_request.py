from typing import Any, Optional

from pydantic import Field

from deps_api_gateway.application.types import FieldType

from ...base import ConfiguredBaseModel

__all__ = ["CreateFieldRequest"]


class CreateFieldRequest(ConfiguredBaseModel):
    name: str
    type: FieldType
    description: Optional[dict[str, Any]] = Field(default=None)
    required: bool
    confidential: bool = Field(default=False)
    read_only: bool = Field(default=False, alias="readOnly")
    order: Optional[int] = Field(default=0)
    extractor_id: Optional[str] = Field(default=None, alias="extractorId")
    field_code: Optional[str] = Field(default=None, alias="code")
