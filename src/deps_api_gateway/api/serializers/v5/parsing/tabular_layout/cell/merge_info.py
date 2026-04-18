from pydantic import Field

from deps_api_gateway.api.serializers import ConfiguredBaseModel

__all__ = ["SerializedMergeInfo"]


class SerializedMergeInfo(ConfiguredBaseModel):
    column_span: int = Field(..., alias="columnSpan")
    row_span: int = Field(..., alias="rowSpan")
