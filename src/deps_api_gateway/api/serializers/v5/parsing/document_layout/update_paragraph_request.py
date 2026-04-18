from pydantic import Field

from ....base import ConfiguredBaseModel
from .point import SerializedPoint

__all__ = ["UpdateParagraphRequest", "SerializedLineUpdateData"]


class SerializedLineUpdateData(ConfiguredBaseModel):
    content: str
    order: int = Field(..., ge=0)
    polygon: list[SerializedPoint] = Field(default_factory=list)


class UpdateParagraphRequest(ConfiguredBaseModel):
    lines: list[SerializedLineUpdateData]
