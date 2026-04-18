from pydantic import Field

from ....base import ConfiguredBaseModel
from .merged_table import SerializedMergedTable
from .page import SerializedPage

__all__ = ["SerializedDocumentLayout"]


class SerializedDocumentLayout(ConfiguredBaseModel):
    id: str = Field(..., alias="documentLayoutId")
    parsing_features: dict[str, list[str]] = Field(..., alias="parsingFeatures")
    merged_tables: dict[str, list[SerializedMergedTable]] = Field(None, alias="mergedTables")
    pages: list[SerializedPage]
