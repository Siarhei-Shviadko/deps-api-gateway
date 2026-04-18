from .....base import ConfiguredBaseModel

__all__ = ["SerializedDimension"]


class SerializedDimension(ConfiguredBaseModel):
    width: int
    height: int
    unit: str
