from pydantic import Field

from deps_api_gateway.api.serializers.base import ConfiguredBaseModel

__all__ = ["SerializedMarkup"]


class SerializedCoordinates(ConfiguredBaseModel):
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    w: float = Field(ge=0, le=1)
    h: float = Field(ge=0, le=1)


class SerializedMarkup(ConfiguredBaseModel):
    code: str
    type: str
    coordinates: list[SerializedCoordinates]
