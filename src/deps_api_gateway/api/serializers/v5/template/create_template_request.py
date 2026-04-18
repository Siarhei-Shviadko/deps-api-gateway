from typing import Optional

from pydantic import Field

from deps_api_gateway.api.serializers.base import ConfiguredBaseModel

__all__ = ["CreateTemplateRequest"]


class CreateTemplateRequest(ConfiguredBaseModel):
    src_template_id: Optional[str] = Field(
        default=None,
        alias="baseTemplateId",
        description="If provided extraction fields will be copied from the base template into the newly created one",
    )
    name: str = Field(..., min_length=1)
    language: str = Field(..., min_length=1)
    engine: str = Field(..., min_length=1)
    description: Optional[str] = Field(default=None, max_length=100)
    group_id: Optional[str] = Field(default=None, alias="groupId")
