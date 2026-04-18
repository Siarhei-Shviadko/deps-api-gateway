from pydantic import Field

from deps_api_gateway.api.serializers import ConfiguredBaseModel

from .cell import SerializedCell

__all__ = ["SerializedTable"]


class SerializedTableSchema(ConfiguredBaseModel):
    id: str
    sheet_id: str = Field(..., alias="sheetId")
    column_count: int = Field(..., alias="columnCount")
    row_count: int = Field(..., alias="rowCount")
    placement: tuple[dict[str, int], dict[str, int]]


class SerializedTable(ConfiguredBaseModel):
    schema_: SerializedTableSchema = Field(..., alias="schema")  # noqa: WPS120
    data: list[SerializedCell]
