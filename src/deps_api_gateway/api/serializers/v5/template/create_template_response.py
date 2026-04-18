from pydantic import Field

from deps_api_gateway.api.serializers.base import ConfiguredBaseModel

__all__ = ["CreateTemplateResponse"]


class CreateTemplateResponse(ConfiguredBaseModel):
    template_id: str = Field(alias="templateId")
