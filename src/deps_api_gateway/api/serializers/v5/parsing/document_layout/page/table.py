from typing import Optional

from pydantic import Field

from .....base import ConfiguredBaseModel
from ..point import SerializedPoint

__all__ = ["SerializedCell", "SerializedTable"]


class SerializedCell(ConfiguredBaseModel):
    content: str
    column_index: int = Field(..., alias="columnIndex")
    column_span: int = Field(..., alias="columnSpan")
    row_index: int = Field(..., alias="rowIndex")
    row_span: int = Field(..., alias="rowSpan")
    kind: Optional[str] = None
    polygon: list[SerializedPoint]
    paragraph_id: Optional[str] = Field(None, alias="paragraphId")


class SerializedTable(ConfiguredBaseModel):
    id: str
    order: int
    confidence: Optional[float] = None
    column_count: int = Field(..., alias="columnCount")
    row_count: int = Field(..., alias="rowCount")
    polygon: list[SerializedPoint]
    cells: list[SerializedCell]
