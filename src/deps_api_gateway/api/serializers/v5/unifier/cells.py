from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedUnifiedDataCell"]


class SerializedWord(ConfiguredBaseModel):
    content: str
    confidence: float


class SerializedCellCoordinates(ConfiguredBaseModel):
    column: int
    row: int
    column_span: int = Field(..., alias="colspan")
    row_span: int = Field(..., alias="rowspan")


class SerializedUnifiedDataCell(ConfiguredBaseModel):
    value: Optional[SerializedWord]
    table_id: str
    coordinates: SerializedCellCoordinates
