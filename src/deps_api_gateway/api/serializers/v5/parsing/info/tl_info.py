from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["SerializerTabularLayoutInfo"]


class SerializedTableInfo(ConfiguredBaseModel):
    id: str
    row_count: int = Field(..., alias="rowCount")
    column_count: int = Field(..., alias="columnCount")


class SerializedSheetInfo(ConfiguredBaseModel):
    id: str
    title: str
    is_hidden: bool = Field(..., alias="isHidden")
    tables: list[SerializedTableInfo]
    images: list[str]


class SerializerTabularLayoutInfo(ConfiguredBaseModel):
    id: str
    parsing_type: str = Field(..., alias="parsingType")
    sheets: list[SerializedSheetInfo]
