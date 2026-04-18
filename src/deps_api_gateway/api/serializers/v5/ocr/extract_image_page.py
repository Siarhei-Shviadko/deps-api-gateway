from typing import List

from pydantic import BaseModel, Field

from .text_line import SerializedTextLine

__all__ = ["ExtractImagePageResponse"]


class ExtractImagePageResponse(BaseModel):
    text_lines: List[SerializedTextLine] = Field(alias="textLines")
