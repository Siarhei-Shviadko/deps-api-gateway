from typing import Optional

from pydantic import Field

from .....base import ConfiguredBaseModel
from ..point import SerializedPoint

__all__ = ["SerializedKeyValuePair"]


class SerializedKeyValuePairElement(ConfiguredBaseModel):
    content: str
    polygon: list[SerializedPoint]
    paragraph_id: Optional[str] = Field(None, alias="paragraphId")


class SerializedKeyValuePair(ConfiguredBaseModel):
    id: str
    key: SerializedKeyValuePairElement
    value: Optional[SerializedKeyValuePairElement] = None
    confidence: float
    order: int
