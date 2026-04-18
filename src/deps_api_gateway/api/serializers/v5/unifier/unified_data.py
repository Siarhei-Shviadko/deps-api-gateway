from typing import Union

from pydantic import Field

from ...base import ConfiguredBaseModel
from .image import SerializedImage
from .positional_text import SerializedPositionalText
from .table import SerializedTable

__all__ = ["SerializedUnifiedData"]

SerializedUnifiedDataElement = Union[SerializedImage, SerializedPositionalText, SerializedTable]


class SerializedUnifiedData(ConfiguredBaseModel):
    document_id: str = Field(..., alias="documentId")
    elements: list[SerializedUnifiedDataElement]
