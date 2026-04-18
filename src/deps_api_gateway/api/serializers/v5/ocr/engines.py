from ...base import ConfiguredBaseModel
from .engine import SerializedOCREngine

__all__ = ["EnginesResponse"]


class EnginesResponse(ConfiguredBaseModel):
    engines: list[SerializedOCREngine]
