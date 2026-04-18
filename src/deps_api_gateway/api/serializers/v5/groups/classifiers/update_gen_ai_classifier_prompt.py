from typing import Optional

from pydantic import Field

from deps_api_gateway.api.serializers.base import ConfiguredBaseModel
from deps_api_gateway.application import GEN_AI_CLASSIFIER_NAME_MAX_LENGTH

__all__ = ["UpdateGenAIClassifierRequest"]


class UpdateGenAIClassifierRequest(ConfiguredBaseModel):
    prompt: Optional[str] = Field(None, min_length=1)
    llm_type: Optional[str] = Field(None, min_length=1)
    name: Optional[str] = Field(None, min_length=1, max_length=GEN_AI_CLASSIFIER_NAME_MAX_LENGTH)
