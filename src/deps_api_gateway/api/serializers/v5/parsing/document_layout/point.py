from ....base import ConfiguredBaseModel

__all__ = ["SerializedPoint"]


class SerializedPoint(ConfiguredBaseModel):
    x: float
    y: float
