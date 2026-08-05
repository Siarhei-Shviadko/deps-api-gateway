from pydantic import Field

from deps_api_gateway.application.parsing.parsing_feature import ParsingFeature
from deps_api_gateway.application.types import NeedsReviewOption

from ...base import ConfiguredBaseModel

__all__ = ["WorkflowConfigurationResponse", "UpdateWorkflowConfigurationRequest", "SerializedWorkflowConfiguration"]


class SerializedWorkflowConfiguration(ConfiguredBaseModel):
    parsing_features: list[ParsingFeature] = Field(..., alias="parsingFeatures")
    needs_postprocessing: bool = Field(..., alias="needsPostprocessing")
    needs_extraction: bool = Field(..., alias="needsExtraction")
    needs_validation: bool = Field(..., alias="needsValidation")
    needs_review: NeedsReviewOption = Field(..., alias="needsReview")
    needs_output_exporting: bool = Field(..., alias="needsOutputExporting")
    engine: str | None = Field(None, alias="engine")


class WorkflowConfigurationResponse(SerializedWorkflowConfiguration):
    document_type_id: str = Field(..., alias="documentTypeId")


class UpdateWorkflowConfigurationRequest(ConfiguredBaseModel):
    parsing_features: set[ParsingFeature] | None = Field(default=None, alias="parsingFeatures")
    needs_postprocessing: bool | None = Field(default=None, alias="needsPostprocessing")
    needs_extraction: bool | None = Field(default=None, alias="needsExtraction")
    needs_validation: bool | None = Field(default=None, alias="needsValidation")
    needs_review: NeedsReviewOption | None = Field(default=None, alias="needsReview")
    needs_output_exporting: bool | None = Field(default=None, alias="needsOutputExporting")
    engine: str | None = Field(default=None, alias="engine")
