from typing import Optional, TypedDict

from .source_bbox_coordinates_data import SourceBboxCoordinatesData
from .source_table_coordinates_data import SourceTableCoordinatesData
from .source_text_coordinates_data import SourceTextCoordinatesData

__all__ = [
    "TableFieldData",
    "TableColumnData",
    "TableRowData",
    "TableCellCoordinatesData",
    "TableCellData",
    "TableMetaData",
]


class TableColumnData(TypedDict):
    x: float


class TableRowData(TypedDict):
    y: float


class TableCellCoordinatesData(TypedDict):
    column: int
    row: int
    column_span: int
    row_span: int


class TableCellData(TypedDict, total=False):
    value: str
    confidence: Optional[float]
    coordinates: TableCellCoordinatesData
    sourceBboxCoordinates: Optional[list[SourceBboxCoordinatesData]]
    sourceTableCoordinates: Optional[list[SourceTableCoordinatesData]]
    sourceTextCoordinates: Optional[list[SourceTextCoordinatesData]]
    pk: Optional[str]


class TableMetaData(TypedDict, total=False):
    chunksTotal: int
    rowsTotal: int
    listIndex: Optional[int]


class TableFieldData(TypedDict, total=False):
    id: Optional[str]
    columns: list[TableColumnData]
    rows: list[TableRowData]
    cells: list[TableCellData]
    sourceBboxCoordinates: Optional[list[SourceBboxCoordinatesData]]
    sourceTableCoordinates: Optional[list[SourceTableCoordinatesData]]
    meta: Optional[TableMetaData]
    paginatedRows: Optional[list[list[TableRowData]]]
