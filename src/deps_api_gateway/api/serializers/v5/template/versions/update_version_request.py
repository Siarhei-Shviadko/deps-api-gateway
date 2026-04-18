from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["UpdateTemplateVersionRequest"]


class UpdateTemplateVersionRequest(ConfiguredBaseModel):
    name: str = Field(..., min_length=1)
