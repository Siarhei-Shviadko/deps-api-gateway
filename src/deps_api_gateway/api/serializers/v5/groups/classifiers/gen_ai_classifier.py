from pydantic import Field

from deps_api_gateway.api.serializers.base import ConfiguredBaseModel

__all__ = ["GenAIClassifierDisplayInfo", "GetClassifiersOfGroupResponse"]


class GenAIClassifierDisplayInfo(ConfiguredBaseModel):
    gen_ai_classifier_id: str = Field(..., alias="genAiClassifierId")
    document_type_id: str = Field(..., alias="documentTypeId")
    prompt: str
    llm_type: str = Field(..., alias="llmType")
    name: str


class GetClassifiersOfGroupResponse(ConfiguredBaseModel):
    gen_ai_classifiers: list[GenAIClassifierDisplayInfo] = Field(..., alias="genAiClassifiers")
