from ......base import ConfiguredBaseModel

__all__ = ["SerializedSignature"]


class SerializedSignature(ConfiguredBaseModel):
    value: str
