from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["UpdateGroupInfoRequest"]


class UpdateGroupInfoRequest(ConfiguredBaseModel):
    name: str = Field(..., min_length=1)
