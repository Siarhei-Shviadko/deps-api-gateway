from typing import Any, Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["UpdateFieldRequest", "UpdateFieldsRequest"]


class UpdateFieldRequest(ConfiguredBaseModel):
    name: Optional[str] = None
    description: Optional[dict[str, Any]] = None
    required: Optional[bool] = None
    read_only: Optional[bool] = Field(default=None, alias="readOnly")
    confidential: Optional[bool] = None
    order: Optional[int] = None


class UpdateFieldWithCodeRequest(UpdateFieldRequest):
    code: str


class UpdateFieldsRequest(ConfiguredBaseModel):
    fields: list[UpdateFieldWithCodeRequest]
