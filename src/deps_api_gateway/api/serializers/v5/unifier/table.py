from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .bbox import SerializedBbox

__all__ = ["SerializedTable"]


class SerializedTable(ConfiguredBaseModel):
    id: str
    page: int
    max_column: int = Field(..., alias="maxColumn")
    max_row: int = Field(..., alias="maxRow")
    coordinates: Optional[SerializedBbox] = None
    name: Optional[str] = None
