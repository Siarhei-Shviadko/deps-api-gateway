from typing import Any, Optional

from pydantic import Field

from deps_api_gateway.application.types import ExtractorType

from ...base import ConfiguredBaseModel

__all__ = ["AttachExtractorRequest"]


class AttachExtractorRequest(ConfiguredBaseModel):
    name: str
    extractor_type: ExtractorType = Field(alias="extractorType")
    engine: Optional[str] = None
    language: Optional[str] = None
    image_transformations: Optional[list[str]] = Field(None, alias="imageTransformations")
    fields: Optional[list[dict[str, Any]]] = Field(default_factory=list)
    description: Optional[str] = Field(None, max_length=100)
