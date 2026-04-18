from typing import Optional

from pydantic import Field

from ......base import ConfiguredBaseModel

__all__ = ["SerializedStyle", "SerializedWord"]


class SerializedStyle(ConfiguredBaseModel):
    background_color: Optional[str] = Field(default=None, alias="backgroundColor")
    color: Optional[str] = None
    bold: bool = False
    italic: bool = False
    handwritten: bool = False
    font_type: Optional[str] = Field(default=None, alias="fontType")
    font_size: Optional[str] = Field(default=None, alias="fontSize")
    underlined: bool = False
    strikeout: bool = False
    subscript: bool = False
    superscript: bool = False
    smallcaps: bool = False


class SerializedWord(ConfiguredBaseModel):
    content: str
    style: SerializedStyle
