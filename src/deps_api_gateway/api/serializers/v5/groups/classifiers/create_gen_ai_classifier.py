from pydantic import Field

from deps_api_gateway.api.serializers.base import ConfiguredBaseModel
from deps_api_gateway.application import GEN_AI_CLASSIFIER_NAME_MAX_LENGTH

__all__ = ["CreateGenAIClassifierRequest", "CreateGenAIClassifierResponse"]


class CreateGenAIClassifierRequest(ConfiguredBaseModel):
    prompt: str = Field(..., min_length=1)
    llm_type: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=GEN_AI_CLASSIFIER_NAME_MAX_LENGTH)


class CreateGenAIClassifierResponse(ConfiguredBaseModel):
    id: str
