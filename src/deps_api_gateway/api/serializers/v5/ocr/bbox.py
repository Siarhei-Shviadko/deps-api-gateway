from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedBbox"]


class SerializedBbox(ConfiguredBaseModel):
    x: float = Field(..., ge=0, le=1)
    y: float = Field(..., ge=0, le=1)
    w: float = Field(..., ge=0, le=1)
    h: float = Field(..., ge=0, le=1)
