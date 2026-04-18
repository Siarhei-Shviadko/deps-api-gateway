from pydantic import Field

from deps_api_gateway.application.document_type import TemplateDataTypeCode

from ...base import ConfiguredBaseModel

__all__ = ["AddMarkupRequest"]


class AddMarkupRequest(ConfiguredBaseModel):
    reference_page: str = Field(..., alias="referencePage")
    markups: dict[str, list[list[float]]] = Field(default_factory=dict)
    markup_types: dict[str, TemplateDataTypeCode] = Field(default_factory=dict, alias="markupTypes")
