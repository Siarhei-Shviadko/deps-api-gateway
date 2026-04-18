from pydantic import Field

from ....base import ConfiguredBaseModel
from ..document_layout import SerializedMergedTable

__all__ = ["SerializedDocumentLayoutInfo"]


class SerializedPageInfo(ConfiguredBaseModel):
    pages_count: int = Field(..., alias="pagesCount")


class SerializedDocumentLayoutInfo(ConfiguredBaseModel):
    id: str = Field(..., alias="documentLayoutId")
    parsing_features: dict[str, list[str]] = Field(..., alias="parsingFeatures")
    merged_tables: dict[str, list[SerializedMergedTable]] = Field(None, alias="mergedTables")
    pages_info: dict[str, SerializedPageInfo] = Field(None, alias="pagesInfo")
