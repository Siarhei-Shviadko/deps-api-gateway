from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["SerializedLabel"]


class SerializedLabel(ConfiguredBaseModel):
    pk: Optional[str] = Field(alias="_id")
    name: str
