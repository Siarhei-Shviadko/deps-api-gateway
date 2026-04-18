from enum import Enum

from deps_api_gateway.application import Header

from ...base import ConfiguredBaseModel

__all__ = [
    "SerializedHeader",
    "HeaderType",
]


class HeaderType(str, Enum):
    ROWS = "rows"
    COLUMNS = "columns"


class SerializedHeader(ConfiguredBaseModel):
    name: str
    aliases: set[str]

    def to_dict(self) -> Header:
        return Header(name=self.name, aliases=list(self.aliases))
