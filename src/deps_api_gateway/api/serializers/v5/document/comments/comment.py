import datetime
from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["SerializedComment"]


class SerializedComment(ConfiguredBaseModel):
    text: str
    created_at: datetime.datetime = Field(alias="createdAt")
    created_by: Optional[str] = Field(None, alias="createdBy")
