from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel
from .source_bbox_coordinates import SerializedSourceBboxCoordinates
from .source_table_coordinates import SerializedSourceTableCoordinates
from .table_cell import SerializedTableCell

__all__ = ["SerializedTableFieldData"]


class SerializedTableColumn(ConfiguredBaseModel):
    x: float = Field(..., ge=0, le=1)


class SerializedTableRow(ConfiguredBaseModel):
    y: float = Field(..., ge=0, le=1)


class SerializedTableMeta(ConfiguredBaseModel):
    chunks_total: int = Field(alias="chunksTotal")
    rows_total: int = Field(alias="rowsTotal")
    list_index: Optional[int] = Field(None, alias="listIndex")


class SerializedTableFieldData(ConfiguredBaseModel):
    id: Optional[str] = Field(None)
    columns: list[SerializedTableColumn]
    rows: list[SerializedTableRow]
    cells: list[SerializedTableCell] = Field(..., description="Cells must contain unique table_cell_coordinates")
    source_bbox_coordinates: Optional[SerializedSourceBboxCoordinates] = Field(
        None,
        alias="sourceBboxCoordinates",
        description="Must have exactly 1 Source Coordinates value",
    )
    source_table_coordinates: Optional[list[SerializedSourceTableCoordinates]] = Field(
        None,
        alias="sourceTableCoordinates",
        description="Must have exactly 1 Source Coordinates value",
    )
    meta: Optional[SerializedTableMeta] = Field(None)
    paginated_rows: Optional[list[list[SerializedTableRow]]] = Field(None, alias="paginatedRows")
