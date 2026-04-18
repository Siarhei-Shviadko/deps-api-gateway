from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["SerializedBbox", "SerializedSourceBboxCoordinates"]


class SerializedBbox(ConfiguredBaseModel):
    y: float
    x: float
    w: float
    h: float


class SerializedSourceBboxCoordinates(ConfiguredBaseModel):
    source_id: str = Field(..., alias="sourceId")
    bboxes: list[SerializedBbox]
