from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import Field

from deps_api_gateway.application import ContextArguments

from ...base import ConfiguredBaseModel

__all__ = [
    "CreateConversationRequest",
    "GetConversationResponse",
    "UpdateConversationRequest",
    "ShortConversationResponse",
    "GetConversationsQuery",
    "GetConversationsResponse",
]


class CreateConversationRequest(ConfiguredBaseModel):
    agent_vendor_id: str = Field(..., alias="agentVendorId")
    mode_id: str = Field(..., alias="modeId")
    title: str
    arguments: ContextArguments
    relation: dict[str, str] | None = None


class ShortConversationResponse(ConfiguredBaseModel):
    id: str


class QuestionSerializer(ConfiguredBaseModel):
    text: str
    created_at: datetime = Field(..., alias="createdAt")


class AnswerSerializer(ConfiguredBaseModel):
    text: str
    created_at: datetime = Field(..., alias="createdAt")


class ExecutionContextSerializer(ConfiguredBaseModel):
    text: str


class RelationSerializer(ConfiguredBaseModel):
    details: dict[str, Any] | None = None


class CompletionSerializer(ConfiguredBaseModel):
    id: str
    question: QuestionSerializer
    execution_context: list[ExecutionContextSerializer] = Field(default_factory=list, alias="executionContext")
    answer: AnswerSerializer | None = None


class GetConversationResponse(ConfiguredBaseModel):
    id: str
    title: str
    relation: RelationSerializer
    completions: list[CompletionSerializer]


class UpdateConversationRequest(ConfiguredBaseModel):
    title: str


class ConversationSortField(str, Enum):
    TITLE = "title"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    AGENT_VENDOR_ID = "agent_vendor_id"


class ConversationSortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class GetConversationsQuery(ConfiguredBaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Items per page")
    mode: str | None = Field(None, min_length=1, description="Filter by mode")
    title: str | None = Field(None, min_length=1, description="Filter by title substring")
    agent_vendor_id: str | None = Field(None, min_length=1, description="Filter by agent vendor id")
    document_id: list[str] | None = Field(None, description="Filter by document IDs", alias="documentId")
    sort_by: ConversationSortField = Field(ConversationSortField.CREATED_AT, description="Sorting field")
    sort_order: ConversationSortOrder = Field(ConversationSortOrder.DESC, description="Sorting order")


class ArgumentSerializer(ConfiguredBaseModel):
    name: str


class ActiveToolSerializer(ConfiguredBaseModel):
    code: str
    arguments: list[ArgumentSerializer]


class ContextSerializer(ConfiguredBaseModel):
    tools: dict[str, list[ActiveToolSerializer]]


class ConversationModeSerializer(ConfiguredBaseModel):
    id: str
    code: str


class ConversationSerializer(ConfiguredBaseModel):
    id: str
    agent_vendor_id: str = Field(..., alias="agentVendorId")
    mode: ConversationModeSerializer
    context: ContextSerializer
    relation: RelationSerializer | None
    title: str
    created_by: str = Field(..., alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class GetConversationsResponse(ConfiguredBaseModel):
    items: dict[str, list[ConversationSerializer]]
    total: int
