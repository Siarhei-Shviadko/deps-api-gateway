from typing import Any, Final, Optional

from pydantic import Field, ValidationInfo, field_validator

from deps_api_gateway.constants import NULL_CONFIDENCE
from deps_api_gateway.domain.exceptions import IllegalArgument

from ....base import ConfiguredBaseModel
from .source_bbox_coordinates import SerializedSourceBboxCoordinates
from .source_table_coordinates import SerializedSourceTableCoordinates
from .source_text_coordinates import SerializedSourceTextCoordinates

__all__ = ["SerializedTableCellCoordinates", "SerializedTableCell"]

SPAN_FIELDS: Final = ("colspan", "rowspan", "column_span", "row_span")  # noqa: WPS407


class SerializedTableCellCoordinates(ConfiguredBaseModel):
    column: int
    row: int
    column_span: int = Field(1, alias="colspan")
    row_span: int = Field(1, alias="rowspan")

    @field_validator("column", "row", "column_span", "row_span", mode="before")
    @classmethod
    def must_be_int(cls, value: Any, field: ValidationInfo) -> int:  # noqa: D401
        name: str = field.field_name

        if not isinstance(value, int) or isinstance(value, bool):
            raise IllegalArgument(f"{name} must be an integer, got {value!r}")

        if name in {"column", "row"} and value < 0:
            raise IllegalArgument(f"{name} must be a non-negative integer, got {value!r}")

        if name in SPAN_FIELDS and value < 1:
            raise IllegalArgument(f"{name} must be a positive integer, got {value!r}")

        return value


class SerializedTableCell(ConfiguredBaseModel):
    id: Optional[str] = Field(None, alias="pk")
    value: str
    confidence: Optional[float] = Field(NULL_CONFIDENCE, le=1.0)
    table_cell_coordinates: SerializedTableCellCoordinates = Field(..., alias="coordinates")
    source_bbox_coordinates: Optional[list[SerializedSourceBboxCoordinates]] = Field(
        None,
        alias="sourceBboxCoordinates",
        description="Must have exactly 1 Source Coordinates value",
    )
    source_table_coordinates: Optional[list[SerializedSourceTableCoordinates]] = Field(
        None,
        alias="sourceTableCoordinates",
        description="Must have exactly 1 Source Coordinates value",
    )
    source_text_coordinates: Optional[list[SerializedSourceTextCoordinates]] = Field(
        None,
        alias="sourceTextCoordinates",
        description="Must have exactly 1 Source Coordinates value",
    )
