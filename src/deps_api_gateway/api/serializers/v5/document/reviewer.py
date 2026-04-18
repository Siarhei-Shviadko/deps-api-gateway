from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedReviewer"]


class SerializedReviewer(ConfiguredBaseModel):
    id: str
    email: Optional[str] = Field(None)
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
