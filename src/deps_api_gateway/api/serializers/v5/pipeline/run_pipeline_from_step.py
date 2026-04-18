from typing import Optional

from pydantic import Field

from deps_api_gateway.application.parsing import ParsingFeature
from deps_api_gateway.application.types import Status

from ...base import ConfiguredBaseModel

__all__ = ["RunPipelineFromStepRequest"]


class RunPipelineFromStepRequest(ConfiguredBaseModel):
    document_ids: list[str] = Field(..., alias="documentIds")
    step: Status
    engine: Optional[str] = Field(None, alias="engineName")
    language: Optional[str] = Field(None)
    llm_type: Optional[str] = Field(None, alias="llmType")
    parsing_features: Optional[set[ParsingFeature]] = Field(None, alias="parsingFeatures")
