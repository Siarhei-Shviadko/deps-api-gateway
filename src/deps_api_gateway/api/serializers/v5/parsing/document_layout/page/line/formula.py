from ......base import ConfiguredBaseModel

__all__ = ["SerializedFormula"]


class SerializedFormula(ConfiguredBaseModel):
    value: str
    kind: str
