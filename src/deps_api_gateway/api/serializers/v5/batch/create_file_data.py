from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["FileRequestSerializer"]


class ProcessingParametersSerializer(ConfiguredBaseModel):
    engine: Optional[str] = Field(None)
    language: Optional[str] = Field(None)
    llm_type: Optional[str] = Field(None, alias="llmType")
    parsing_features: Optional[list[str]] = Field(None, alias="parsingFeatures")


class FileRequestSerializer(ConfiguredBaseModel):
    name: str
    path: str
    document_type_id: Optional[str] = Field(None, alias="documentTypeId")
    processing_params: ProcessingParametersSerializer = Field(..., alias="processingParams")
