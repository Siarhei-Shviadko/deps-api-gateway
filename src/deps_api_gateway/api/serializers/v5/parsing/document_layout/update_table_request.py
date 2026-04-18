from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["UpdateTableRequest"]


class SerializedCellUpdateData(ConfiguredBaseModel):
    content: str
    row_index: int = Field(..., alias="rowIndex")
    column_index: int = Field(..., alias="columnIndex")


class UpdateTableRequest(ConfiguredBaseModel):
    cells: list[SerializedCellUpdateData]
