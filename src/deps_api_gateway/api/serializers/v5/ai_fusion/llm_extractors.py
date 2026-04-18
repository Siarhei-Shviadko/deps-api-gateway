from typing import Any, Optional, Self

from pydantic import Field, model_validator

from deps_api_gateway.domain import ContextAttachments

from ...base import ConfiguredBaseModel
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
DEFAULT_TEMPERATURE: float = 0
DEFAULT_TOP_P: float = 1.0


class SerializedPageSpan(ConfiguredBaseModel):
    start: int = Field(..., ge=1)
    end: int = Field(..., ge=1)

    @model_validator(mode="after")
    def check_order(self) -> Self:
        if self.start is not None and self.end is not None and self.start > self.end:
            raise ValueError("PageSpan start must be less or equal end!")
        return self

    def to_dict(self) -> dict[str, Any]:
        return {"start": self.start, "end": self.end}


class SerializedLLMExtractionParams(ConfiguredBaseModel):
    custom_instruction: str = Field(DEFAULT_CUSTOM_INSTRUCTION, alias="customInstruction")
    grouping_factor: int = Field(DEFAULT_GROUPING_FACTOR, alias="groupingFactor", ge=1)
    temperature: float = Field(DEFAULT_TEMPERATURE, ge=0, le=2)
    top_p: float = Field(DEFAULT_TOP_P, alias="topP", ge=0, le=1)
    page_span: SerializedPageSpan | None = Field(None, alias="pageSpan")
    context_attachments: ContextAttachments | None = Field(None, alias="contextAttachments")

    def to_dict(self) -> dict[str, Any]:
        return {
            "customInstruction": self.custom_instruction,
            "groupingFactor": self.grouping_factor,
            "temperature": self.temperature,
            "topP": self.top_p,
            "pageSpan": self.page_span.to_dict() if self.page_span else None,
            "contextAttachments": self.context_attachments.value if self.context_attachments else None,
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


class UpdateExtractorParams(ConfiguredBaseModel):
    custom_instruction: str = Field(..., alias="customInstruction")
    grouping_factor: int = Field(..., ge=1, alias="groupingFactor")
    temperature: float = Field(..., ge=0, le=2)
    top_p: float = Field(..., ge=0, le=1, alias="topP")
    page_span: Optional[SerializedPageSpan] = Field(..., alias="pageSpan")
    context_attachments: ContextAttachments | None = Field(None, alias="contextAttachments")


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
