from typing import Optional

from .....base import ConfiguredBaseModel
from ..point import SerializedPoint
from .line import SerializedLine

__all__ = ["SerializedParagraph"]


class SerializedParagraph(ConfiguredBaseModel):
    id: str
    order: int
    content: str
    confidence: Optional[float] = None
    role: Optional[str] = None
    polygon: list[SerializedPoint]
    lines: list[SerializedLine]
