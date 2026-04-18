from pydantic import Field

from ...base import ConfiguredBaseModel
from .bbox import SerializedBbox

__all__ = ["SerializedWordBox"]


class SerializedWordBox(ConfiguredBaseModel):
    content: str
    bbox: SerializedBbox
    confidence: float = Field(1.0, ge=0, le=1.0)
