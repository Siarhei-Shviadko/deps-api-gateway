from typing import Any, Union

from pydantic import Field

from ...base import ConfiguredBaseModel
from .base_llm_params import BaseLLMParams
from .llm_extractors import SerializedPageSpan

__all__ = ["RetrieveInsightsRequest", "RetrieveInsightsResponse", "RetrieveFileInsightsRequest"]


class SerializedGenAIPrompt(ConfiguredBaseModel):
    content: str


class SerializedGenAIWorkflow(ConfiguredBaseModel):
    prompts: list[SerializedGenAIPrompt]
    response_model: dict[str, Any] | None = Field(
        None,
        alias="responseModel",
        description="A JSON Schema (OpenAPI V3) object defining the shape of the LLM’s structured response..",
    )


class SerializedGenAIQuery(ConfiguredBaseModel):
    workflow: SerializedGenAIWorkflow


class RetrieveInsightsRequestParams(BaseLLMParams):
    grouping_factor: int | None = Field(
        None,
        alias="groupingFactor",
        description="""Defines how many elements are grouped per LLM request.
        The higher this value, the fewer requests will be made to the LLM decreasing costs (as document context is loaded into each request).
        On the other hand, a large number of elements grouped in a single request potentially decreases the quality of the insights retrieved.
        """,
    )
    page_span: SerializedPageSpan | None = Field(
        None,
        alias="pageSpan",
        description="Inclusive range of pages to process. If omitted, all pages will be processed.",
    )


class RetrieveInsightsRequest(ConfiguredBaseModel):
    model: str = Field(
        ...,
        alias="model",
        description="LLM Reference contains information about Provider and Model in the format of 'provider@model'",
    )
    requested_insights: dict[str, Union[str, SerializedGenAIQuery]] = Field(
        ...,
        alias="requestedInsights",
        description="Mapping between an ElementCode to retrieve insights for, and a LLM Query to use for that ElementCode",
    )

    custom_instructions: str | None = Field(
        None,
        alias="customInstructions",
        description="""Custom instructions are appended to the system prompt to guide the model’s behavior.
        Useful for adapting the model to specific use cases, such as summarization, extraction, classification, etc.
        They also help to tailor the responses by specifying constraints, response style, or additional context.
        """,
    )
    params: RetrieveInsightsRequestParams = Field(
        ...,
        description="Additional parameters to be used for the insights retrieval.",
    )
    files: list[str] | None = Field(None, description="Paths to files, that will be added to context.")

    def requested_insights_to_dict(self) -> dict[str, Union[str, dict[str, Any]]]:
        return {
            key: value if isinstance(value, str) else value.model_dump(by_alias=True)
            for key, value in self.requested_insights.items()
        }


class RetrieveFileInsightsRequest(RetrieveInsightsRequest):
    file_path: str = Field(
        ...,
        alias="filePath",
        description="The path from DEPS File Storage to be recognized.",
    )


class Insight(ConfiguredBaseModel):
    content: str
    confidence: float | None = Field(None, description="Confidence score for the insight.")


class RetrieveInsightsResponse(ConfiguredBaseModel):
    elements: dict[str, Insight]
