from typing import Optional, TypedDict

__all__ = ["SourceTableCoordinatesData", "CellCoordinatesData", "CellRangeData"]


class CellCoordinatesData(TypedDict):
    column: int
    row: int


class CellRangeData(TypedDict, total=False):
    begin: CellCoordinatesData
    end: Optional[CellCoordinatesData]


class SourceTableCoordinatesData(TypedDict):
    sourceId: str
    cellRanges: list[CellRangeData]
