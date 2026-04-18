from typing import Optional, Self

from pydantic import Field, model_validator

from ...base import ConfiguredBaseModel
from .header import HeaderType, SerializedHeader

__all__ = [
    "CreateTabularMappingRequest",
    "SerializedTabularMapping",
    "UpdateTabularMappingRequest",
]


class SerializedTabularMapping(ConfiguredBaseModel):
    code: str
    prototype_id: str = Field(..., alias="prototypeId")
    headers: list[SerializedHeader]
    header_type: HeaderType = Field(..., alias="headerType")
    occurrence_index: int = Field(
        ...,
        alias="occurrenceIndex",
        description="Index of the found item to return if multiple elements were mapped for current TabularMapping, "
        "but one has to be returned",
    )


class CreateTabularMappingRequest(ConfiguredBaseModel):
    code: str
    header_type: HeaderType = Field(..., alias="headerType")
    headers: list[SerializedHeader]
    occurrence_index: int = Field(0, alias="occurrenceIndex")

    @model_validator(mode="after")
    def check_headers_not_empty(self) -> Self:  # noqa: N805, WPS110
        if not self.headers:
            raise ValueError("Headers must contain at least one item")
        return self


class UpdateTabularMappingRequest(ConfiguredBaseModel):
    header_type: Optional[HeaderType] = Field(None, alias="headerType")
    headers: Optional[list[SerializedHeader]] = Field(None, min_length=1)
    occurrence_index: Optional[int] = Field(None, alias="occurrenceIndex")
