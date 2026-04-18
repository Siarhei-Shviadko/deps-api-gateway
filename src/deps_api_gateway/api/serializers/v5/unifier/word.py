from ...base import ConfiguredBaseModel

__all__ = ["SerializedWord"]


class SerializedWord(ConfiguredBaseModel):
    content: str
    confidence: float
