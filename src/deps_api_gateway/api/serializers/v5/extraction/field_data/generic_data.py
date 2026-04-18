from typing import Optional, Union

from pydantic import Field, StrictStr

from deps_api_gateway.application.types import CheckboxValue
from deps_api_gateway.constants import NULL_CONFIDENCE

from ....base import ConfiguredBaseModel
from .source_bbox_coordinates import SerializedSourceBboxCoordinates
from .source_table_coordinates import SerializedSourceTableCoordinates
from .source_text_coordinates import SerializedSourceTextCoordinates

__all__ = ["SerializedGenericData"]


class SerializedGenericData(ConfiguredBaseModel):
    id: Optional[str] = None
    value: Union[CheckboxValue, StrictStr]
    confidence: Optional[float] = Field(NULL_CONFIDENCE, le=1.0)
    source_bbox_coordinates: Optional[list[SerializedSourceBboxCoordinates]] = Field(
        None, alias="sourceBboxCoordinates", description="Can only have 1 Source Coordinates value"
    )
    source_table_coordinates: Optional[list[SerializedSourceTableCoordinates]] = Field(
        None, alias="sourceTableCoordinates", description="Can only have 1 Source Coordinates value"
    )
    source_text_coordinates: Optional[list[SerializedSourceTextCoordinates]] = Field(
        None, alias="sourceTextCoordinates", description="Can only have 1 Source Coordinates value"
    )
    coordinates: Optional[dict] = None
    table_coordinates: Optional[list] = Field(default_factory=list, alias="tableCoordinates")
