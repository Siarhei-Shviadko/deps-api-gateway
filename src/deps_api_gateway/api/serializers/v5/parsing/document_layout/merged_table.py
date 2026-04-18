from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["SerializedMergedTable"]


class SerializedTableReference(ConfiguredBaseModel):
    page_number: int = Field(..., alias="pageNumber")
    table_id: str = Field(..., alias="tableId")


class SerializedMergedTable(ConfiguredBaseModel):
    parsing_type: str = Field(..., alias="parsingType")
    tables: list[SerializedTableReference]
