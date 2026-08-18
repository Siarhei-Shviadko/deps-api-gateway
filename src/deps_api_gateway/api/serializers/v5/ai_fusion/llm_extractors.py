from typing import Any

from pydantic import Field

from deps_api_gateway.domain import ContextAttachments

from ...base import ConfiguredBaseModel
from .base_llm_params import BaseLLMParams
from .page_span import SerializedPageSpan
from .query import SerializedExtractionQuery

__all__ = [
    "AttachLLMExtractorRequest",
    "AttachLLMExtractorResponse",
    "UpdateLLMExtractorRequest",
    "UpdateLLMExtractorResponse",
    "SerializedLLMExtractor",
    "AssignLLMToLLMExtractorRequest",
    "AssignLLMToLLMExtractorResponse",
]


DEFAULT_CUSTOM_INSTRUCTION: str = """\
For the provided document context and based on the specific user instructions, analyze and extract relevant insights.
Focus on identifying actionable, relevant, and concise information that fulfills the purpose of the instructions.
Ensure that the extracted insights are accurate, adhere to specified constraints and respond strictly in the format requested.\
"""
DEFAULT_GROUPING_FACTOR: int = 3
DEFAULT_TEMPERATURE: float = 0.5


class SerializedLLMExtractionParams(BaseLLMParams):
    custom_instruction: str = Field(DEFAULT_CUSTOM_INSTRUCTION, alias="customInstruction")
    grouping_factor: int = Field(DEFAULT_GROUPING_FACTOR, alias="groupingFactor", ge=1)
    page_span: SerializedPageSpan | None = Field(None, alias="pageSpan")
    context_attachments: ContextAttachments | None = Field(None, alias="contextAttachments")
    coordinates_enabled: bool = Field(
        default=False,
        alias="coordinatesEnabled",
        description="Enables automatic source-coordinate enrichment for every query in the extractor",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "customInstruction": self.custom_instruction,
            "groupingFactor": self.grouping_factor,
            "temperature": self.temperature,
            "topP": self.top_p,
            "maxTokens": self.max_tokens,
            "stop": self.stop,
            "seed": self.seed,
            "logprobs": self.logprobs,
            "extraModelParams": self.extra_model_params,
            "pageSpan": self.page_span.to_dict() if self.page_span else None,
            "contextAttachments": self.context_attachments.value if self.context_attachments else None,
            "coordinatesEnabled": self.coordinates_enabled,
        }


class AttachLLMExtractorRequest(ConfiguredBaseModel):
    extractor_name: str = Field(..., alias="extractorName")
    extractor_id: str | None = Field(default=None, alias="extractorId")
    document_type_name: str = Field(..., alias="documentTypeName")
    provider: str
    model: str

    extraction_params: SerializedLLMExtractionParams = Field(..., alias="extractionParams")


class AttachLLMExtractorResponse(ConfiguredBaseModel):
    extractor_id: str = Field(..., alias="extractorId")
    document_type_id: str = Field(..., alias="documentTypeId")


class UpdateExtractorParams(BaseLLMParams):
    custom_instruction: str = Field(..., alias="customInstruction")
    grouping_factor: int = Field(..., ge=1, alias="groupingFactor")
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        ge=0,
        le=2,
        examples=[0.7],
        description="""Controls the randomness of text generation.
        Lower temperatures make the model more deterministic and repetitive,
         while higher temperatures make the model more creative and random.
        """,
    )
    page_span: SerializedPageSpan | None = Field(..., alias="pageSpan")
    context_attachments: ContextAttachments | None = Field(None, alias="contextAttachments")
    coordinates_enabled: bool = Field(
        default=False,
        alias="coordinatesEnabled",
        description="Enables automatic source-coordinate enrichment for every query in the extractor",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "customInstruction": self.custom_instruction,
            "groupingFactor": self.grouping_factor,
            "temperature": self.temperature,
            "topP": self.top_p,
            "maxTokens": self.max_tokens,
            "stop": self.stop,
            "seed": self.seed,
            "logprobs": self.logprobs,
            "extraModelParams": self.extra_model_params,
            "pageSpan": self.page_span.to_dict() if self.page_span else None,
            "contextAttachments": self.context_attachments.value if self.context_attachments else None,
            "coordinatesEnabled": self.coordinates_enabled,
        }


class UpdateLLMExtractorRequest(ConfiguredBaseModel):
    name: str
    extraction_params: UpdateExtractorParams = Field(..., alias="extractionParams")


class UpdateLLMExtractorResponse(ConfiguredBaseModel):
    extractor_id: str = Field(..., alias="extractorId")
    document_type_id: str = Field(..., alias="documentTypeId")


class AssignLLMToLLMExtractorRequest(ConfiguredBaseModel):
    provider: str
    model: str


class AssignLLMToLLMExtractorResponse(ConfiguredBaseModel):
    extractor_id: str = Field(..., alias="extractorId")
    document_type_id: str = Field(..., alias="documentTypeId")


class SerializedLLMExtractor(ConfiguredBaseModel):
    extractor_id: str = Field(..., alias="extractorId")
    name: str
    provider: str
    model: str
    queries: list[SerializedExtractionQuery]

    extraction_params: SerializedLLMExtractionParams = Field(..., alias="extractionParams")
