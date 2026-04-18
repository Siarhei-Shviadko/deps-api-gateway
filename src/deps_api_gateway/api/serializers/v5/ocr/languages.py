from ...base import ConfiguredBaseModel
from .language import SerializedLanguage

__all__ = ["LanguagesResponse"]


class LanguagesResponse(ConfiguredBaseModel):
    languages: list[SerializedLanguage]
