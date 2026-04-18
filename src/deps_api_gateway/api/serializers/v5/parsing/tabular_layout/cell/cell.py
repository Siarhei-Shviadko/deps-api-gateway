from typing import Optional

from pydantic import Field

from deps_api_gateway.api.serializers import ConfiguredBaseModel

from .alignment import SerializedAlignment
from .borders import SerializedBorders
from .comment import SerializedComment
from .merge_info import SerializedMergeInfo
from .style import SerializedStyle

__all__ = ["SerializedCell"]


class SerializedCell(ConfiguredBaseModel):
    id: str
    table_id: str = Field(..., alias="tableId")
    content: str
    data_type: str = Field(None, alias="dataType")
    relative_position: tuple[int, int] = Field(..., alias="relativePosition")
    absolute_position: tuple[int, int] = Field(..., alias="absolutePosition")
    merge: Optional[SerializedMergeInfo] = None
    style: Optional[SerializedStyle] = None
    comment: Optional[SerializedComment] = None
    alignment: Optional[SerializedAlignment] = None
    borders: Optional[SerializedBorders] = None
