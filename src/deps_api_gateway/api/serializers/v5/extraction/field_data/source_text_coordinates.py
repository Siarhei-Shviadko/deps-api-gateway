from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["SerializedCharRange", "SerializedSourceTextCoordinates"]


class SerializedCharRange(ConfiguredBaseModel):
    begin: int = Field(..., ge=0)
    end: int = Field(..., ge=0)


class SerializedSourceTextCoordinates(ConfiguredBaseModel):
    source_id: str = Field(..., alias="sourceId")
    char_ranges: list[SerializedCharRange] = Field(..., alias="charRanges")
