from typing import Optional

from pydantic import Field

from deps_api_gateway.api.serializers import ConfiguredBaseModel

__all__ = ["SerializedStyle"]


class SerializedStyle(ConfiguredBaseModel):
    background_color: Optional[str] = Field(None, alias="backgroundColor")
    color: Optional[str] = None
    hyperlink: Optional[bool] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    font_name: Optional[str] = Field(None, alias="fontName")
    font_size: Optional[str] = Field(None, alias="fontSize")
    underlined: Optional[bool] = None
    strikethrough: Optional[bool] = None
