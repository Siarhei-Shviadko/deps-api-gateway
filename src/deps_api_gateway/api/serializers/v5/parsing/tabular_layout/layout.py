from pydantic import Field

from deps_api_gateway.api.serializers import ConfiguredBaseModel

from .sheet import SerializedSheet
from .table import SerializedTable

__all__ = ["SerializedTabularLayout"]


class SerializedTabularLayout(ConfiguredBaseModel):
    id: str
    tenant_id: str = Field(..., alias="tenantId")
    parsing_type: str = Field(..., alias="parsingType")
    extracted_properties: list[str] = Field(default_factory=list, alias="extractedProperties")
    sheets: dict[str, SerializedSheet]
    tables: dict[str, SerializedTable]
