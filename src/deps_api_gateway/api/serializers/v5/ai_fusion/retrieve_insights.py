from typing import Any, Optional, Union

from pydantic import Field

from ...base import ConfiguredBaseModel
from .llm_extractors import SerializedPageSpan

__all__ = ["RetrieveInsightsRequest", "RetrieveInsightsResponse", "RetrieveFileInsightsRequest"]


class SerializedGenAIPrompt(ConfiguredBaseModel):
    content: str


class SerializedGenAIWorkflow(ConfiguredBaseModel):
    prompts: list[SerializedGenAIPrompt]
    response_model: Optional[dict[str, Any]] = Field(
        None,
        alias="responseModel",
        description="A JSON Schema (OpenAPI V3) object defining the shape of the LLM’s structured response..",
    )


class SerializedGenAIQuery(ConfiguredBaseModel):
    workflow: SerializedGenAIWorkflow


class RetrieveInsightsRequestParams(ConfiguredBaseModel):
    temperature: float = Field(
        default=0,
        description="""Controls the randomness of text generation.
        Lower temperatures make the model more deterministic and repetitive, while higher temperatures make the model more creative and random.
        """,
    )
    top_p: float = Field(
        default=1,
        alias="topP",
        description="""Controls diversity via nucleus sampling.
        Only tokens with cumulative probability mass of top_p are considered. Value must be between 0 and 1.
        Lower values make output more focused and deterministic.
        """,
    )
    grouping_factor: Optional[int] = Field(
        None,
        alias="groupingFactor",
        description="""Defines how many elements are grouped per LLM request.
        The higher this value, the fewer requests will be made to the LLM decreasing costs (as document context is loaded into each request).
        On the other hand, a large number of elements grouped in a single request potentially decreases the quality of the insights retrieved.
        """,
    )
    page_span: Optional[SerializedPageSpan] = Field(
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

    custom_instructions: Optional[str] = Field(
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
    files: Optional[list[str]] = Field(None, description="Paths to files, that will be added to context.")

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
    confidence: Optional[float]


class RetrieveInsightsResponse(ConfiguredBaseModel):
    elements: dict[str, Insight]
