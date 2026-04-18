from ...base import ConfiguredBaseModel

__all__ = ["SerializedBbox"]


class SerializedBbox(ConfiguredBaseModel):
    x: float
    y: float
    w: float
    h: float
