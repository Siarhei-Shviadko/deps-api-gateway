from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = [
    "CreateAzureExtractorRequest",
    "CreateAzureExtractorRespose",
    "AzureExtractorInfoResponse",
    "ValidateAzureCredentialsRequest",
    "UpdateAzureExtractorRequest",
    "AzureExtractorHealthcheckResponse",
]


class CreateAzureExtractorRequest(ConfiguredBaseModel):
    name: str
    model_id: str = Field(..., alias="modelId")
    endpoint: str
    api_key: str = Field(..., alias="apiKey")
    language: Optional[str] = None
    description: Optional[str] = None


class CreateAzureExtractorRespose(ConfiguredBaseModel):
    extractor_id: str = Field(..., alias="extractorId")


class AzureExtractorInfoResponse(ConfiguredBaseModel):
    id: str
    model_id: str = Field(..., alias="modelId")
    endpoint: str


class ValidateAzureCredentialsRequest(ConfiguredBaseModel):
    model_id: str = Field(..., alias="modelId")
    endpoint: str
    api_key: str = Field(..., alias="apiKey")


class UpdateAzureExtractorRequest(ConfiguredBaseModel):
    model_id: str = Field(..., alias="modelId")
    endpoint: str
    api_key: str = Field(..., alias="apiKey")


class AzureExtractorHealthcheckResponse(ConfiguredBaseModel):
    status: str
    description: str
