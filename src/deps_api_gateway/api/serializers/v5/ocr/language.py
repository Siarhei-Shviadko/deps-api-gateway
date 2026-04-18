from ...base import ConfiguredBaseModel

__all__ = ["SerializedLanguage"]


class SerializedLanguage(ConfiguredBaseModel):
    code: str
    name: str
