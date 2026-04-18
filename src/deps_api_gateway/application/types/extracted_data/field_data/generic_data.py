from typing import Optional, TypedDict, Union

from deps_api_gateway.application.types import CheckboxValue

from .source_bbox_coordinates_data import SourceBboxCoordinatesData
from .source_table_coordinates_data import SourceTableCoordinatesData
from .source_text_coordinates_data import SourceTextCoordinatesData

__all__ = ["GenericData"]


class GenericData(TypedDict, total=False):
    id: Optional[str]
    value: Union[CheckboxValue, str]
    confidence: Optional[float]
    sourceBboxCoordinates: Optional[list[SourceBboxCoordinatesData]]
    sourceTableCoordinates: Optional[list[SourceTableCoordinatesData]]
    sourceTextCoordinates: Optional[list[SourceTextCoordinatesData]]
    coordinates: Optional[dict]
    tableCoordinates: Optional[list]
