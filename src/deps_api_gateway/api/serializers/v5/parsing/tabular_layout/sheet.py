from pydantic import Field

from deps_api_gateway.api.serializers import ConfiguredBaseModel

from .image import SerializedImage

__all__ = ["SerializedSheet"]


class SerializedSheet(ConfiguredBaseModel):
    id: str
    title: str
    is_hidden: bool = Field(..., alias="isHidden")
    images: list[SerializedImage]
    table_ids: list[str] = Field(..., alias="tableIds")
