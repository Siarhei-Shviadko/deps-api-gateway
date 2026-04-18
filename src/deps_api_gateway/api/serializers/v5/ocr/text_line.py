from pydantic import Field

from ...base import ConfiguredBaseModel
from .word_box import SerializedWordBox

__all__ = ["SerializedTextLine"]


class SerializedTextLine(ConfiguredBaseModel):
    id: int
    word_boxes: list[SerializedWordBox] = Field(..., alias="wordBoxes")
