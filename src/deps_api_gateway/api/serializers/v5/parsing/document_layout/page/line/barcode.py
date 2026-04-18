from ......base import ConfiguredBaseModel

__all__ = ["SerializedBarcode"]


class SerializedBarcode(ConfiguredBaseModel):
    value: str
    kind: str
