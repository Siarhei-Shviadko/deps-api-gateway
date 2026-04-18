from typing import Optional, TypedDict

__all__ = ["CellsReference"]


class CellsReference(TypedDict, total=False):
    firstColumn: Optional[int]
    lastColumn: Optional[int]
    firstRow: Optional[int]
    lastRow: Optional[int]
