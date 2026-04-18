from pydantic import Field

from ...base import ConfiguredBaseModel
from .completion import SerializedCompletion
from .provider import SerializedProvider

__all__ = ["SerializedConversation", "SerializedConversationInfo"]


class SerializedConversation(ConfiguredBaseModel):
    entity_id: str = Field(..., alias="entityId")
    tenant_id: str = Field(..., alias="tenantId")
    user_id: str = Field(..., alias="userId")
    completions: list[SerializedCompletion]


class SerializedConversationInfo(ConfiguredBaseModel):
    conversation: SerializedConversation
    providers: list[SerializedProvider]
