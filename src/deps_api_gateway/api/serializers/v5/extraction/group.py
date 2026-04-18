from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedGroup"]


class SerializedGroup(ConfiguredBaseModel):
    order: int
    name: str
    elements: list[str] = Field(default_factory=list)
