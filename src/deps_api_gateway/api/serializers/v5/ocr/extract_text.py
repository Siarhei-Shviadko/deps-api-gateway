from pydantic import Field

from ...base import ConfiguredBaseModel
from .text_line import SerializedTextLine

__all__ = ["ExtractTextResponse"]


class ExtractTextResponse(ConfiguredBaseModel):
    text_lines: list[SerializedTextLine] = Field(alias="textLines")
