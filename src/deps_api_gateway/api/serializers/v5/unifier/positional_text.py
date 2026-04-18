from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .word_box import SerializedWordBox

__all__ = ["SerializedPositionalText"]


class SerializedPositionalText(ConfiguredBaseModel):
    id: str
    image_id: Optional[str] = Field(None, alias="imageId")
    page: int
    wordboxes: list[SerializedWordBox]
