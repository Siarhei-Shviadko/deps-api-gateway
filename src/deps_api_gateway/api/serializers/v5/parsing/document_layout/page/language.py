from pydantic import Field

from .....base import ConfiguredBaseModel

__all__ = ["SerializedLanguage"]


class SerializedLanguage(ConfiguredBaseModel):
    language_code: str = Field(..., alias="languageCode")
    confidence: float
