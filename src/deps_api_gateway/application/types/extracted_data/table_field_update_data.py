from typing import TypedDict

from .field_data import TableCellData

__all__ = ["TableFieldUpdateData"]


class TableFieldUpdateData(TypedDict):
    cells: list[TableCellData]
