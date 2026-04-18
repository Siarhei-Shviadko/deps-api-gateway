from datetime import datetime
from typing import Optional

from pydantic import Field

from deps_api_gateway.api.serializers.base import ConfiguredBaseModel

__all__ = ["TemplateVersionsList"]


class ShortTemplateVersion(ConfiguredBaseModel):
    id: str
    name: str
    created_at: datetime = Field(..., alias="createdAt")
    description: Optional[str]


class TemplateVersionsList(ConfiguredBaseModel):
    versions: list[ShortTemplateVersion]
