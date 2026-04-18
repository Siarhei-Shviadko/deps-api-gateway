from typing import Optional

from pydantic import Field

from ..ai_fusion import SerializedLLMExtractor
from ..enrichment import SerializedExtraField
from ..extraction_fields import SerializedField
from ..groups import GetClassifiersOfGroupResponse
from ..output_exporting import SerializedOutputProfile
from ..validation import SerializedCrossFieldValidator, SerializedValidator
from .document_type import SerializedDocumentType

__all__ = ["GetDocumentTypeResponse"]


class GetDocumentTypeResponse(SerializedDocumentType):
    extraction_fields: Optional[list[SerializedField]] = Field(..., alias="extractionFields")
    extra_fields: Optional[list[SerializedExtraField]] = Field(..., alias="extraFields")
    validators: Optional[list[SerializedValidator]]
    cross_field_validators: Optional[list[SerializedCrossFieldValidator]] = Field(..., alias="crossFieldValidators")
    profiles: Optional[list[SerializedOutputProfile]]
    classifiers: Optional[GetClassifiersOfGroupResponse]
    llm_extractors: Optional[list[SerializedLLMExtractor]] = Field(..., alias="llmExtractors")
