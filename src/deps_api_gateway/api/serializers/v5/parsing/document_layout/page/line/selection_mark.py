from ......base import ConfiguredBaseModel

__all__ = ["SerializedSelectionMark"]


class SerializedSelectionMark(ConfiguredBaseModel):
    state: str
