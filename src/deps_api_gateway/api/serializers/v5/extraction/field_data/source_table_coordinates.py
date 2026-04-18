from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = [
    "SerializedCellCoordinates",
    "SerializedCellRange",
    "SerializedSourceTableCoordinates",
]


class SerializedCellCoordinates(ConfiguredBaseModel):
    column: int = Field(..., ge=0)
    row: int = Field(..., ge=0)


class SerializedCellRange(ConfiguredBaseModel):
    begin: SerializedCellCoordinates
    end: Optional[SerializedCellCoordinates]


class SerializedSourceTableCoordinates(ConfiguredBaseModel):
    source_id: str = Field(..., alias="sourceId")
    cell_ranges: list[SerializedCellRange] = Field(..., alias="cellRanges")
