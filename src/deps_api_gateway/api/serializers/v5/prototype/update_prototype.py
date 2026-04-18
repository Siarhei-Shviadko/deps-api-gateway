from datetime import datetime

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["UpdatePrototypeRequest", "UpdatePrototypeResponse"]


class UpdatePrototypeRequest(ConfiguredBaseModel):
    engine: str | None = None
    language: str | None = None
    description: str | None = None


class UpdatePrototypeResponse(ConfiguredBaseModel):
    id: str
    name: str
    engine: str
    language: str
    created_at: datetime = Field(..., alias="createdAt")
    description: str | None = None
