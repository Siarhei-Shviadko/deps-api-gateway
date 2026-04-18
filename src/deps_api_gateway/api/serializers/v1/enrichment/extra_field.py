from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SaveExtraFieldRequest", "UpdateExtraFieldsRequest"]


class SaveExtraFieldRequest(ConfiguredBaseModel):
    name: str
    display_order: int = Field(default=0, alias="order")


class UpdateExtraFieldRequest(ConfiguredBaseModel):
    code: str
    name: Optional[str]
    display_order: Optional[int] = Field(default=None, alias="order")


class UpdateExtraFieldsRequest(ConfiguredBaseModel):
    extra_fields: list[UpdateExtraFieldRequest]
