from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response, status

from deps_api_gateway.application import AgenticAIService
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    CompletionsResponse,
    CreateConversationRequest,
    GetConversationResponse,
    GetConversationsQuery,
    GetConversationsResponse,
    ShortConversationResponse,
    UpdateConversationRequest,
)
from ....utilities import ResponseBuilder
from .constants import (
    PAGINATION_DEFAULT_PAGE,
    PAGINATION_DEFAULT_PER_PAGE,
    PAGINATION_MIN_PAGE,
    PAGINATION_MIN_PER_PAGE,
)

__all__ = ["conversations_router"]

conversations_router = APIRouter(prefix="/conversations", tags=["Conversations"])


@conversations_router.post("", status_code=status.HTTP_201_CREATED, response_model=ShortConversationResponse)
@inject
async def create_conversation(
    conversation: CreateConversationRequest,
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.create_conversation(
        agent_vendor_id=conversation.agent_vendor_id,
        mode_id=conversation.mode_id,
        title=conversation.title,
        arguments=conversation.arguments,
        relation=conversation.relation,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversations_router.get("/{conversationId}", status_code=status.HTTP_200_OK, response_model=GetConversationResponse)
@inject
async def get_conversation(
    conversation_id: str = Path(..., alias="conversationId"),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.get_conversation(conversation_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversations_router.get("", status_code=status.HTTP_200_OK, response_model=GetConversationsResponse)
@inject
async def get_conversations(
    query: Annotated[GetConversationsQuery, Query()],
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.get_conversations(
        page=query.page,
        size=query.size,
        sort_by=query.sort_by.value,
        sort_order=query.sort_order.value,
        mode=query.mode,
        title=query.title,
        agent_vendor_id=query.agent_vendor_id,
        document_ids=query.document_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversations_router.get(
    "/{conversationId}/completions",
    status_code=status.HTTP_200_OK,
    response_model=CompletionsResponse,
)
@inject
async def get_conversation_completions(
    conversation_id: str = Path(..., alias="conversationId"),
    page: int = Query(default=PAGINATION_DEFAULT_PAGE, ge=PAGINATION_MIN_PAGE),
    per_page: int = Query(default=PAGINATION_DEFAULT_PER_PAGE, alias="perPage", ge=PAGINATION_MIN_PER_PAGE),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
):
    proxy_response = await application.get_completions(
        conversation_id=conversation_id,
        page=page,
        per_page=per_page,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversations_router.patch(
    "/{conversationId}",
    status_code=status.HTTP_200_OK,
    response_model=ShortConversationResponse,
)
@inject
async def update_conversation(
    data_request: UpdateConversationRequest,
    conversation_id: str = Path(..., alias="conversationId"),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.update_conversation(
        conversation_id=conversation_id,
        title=data_request.title,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversations_router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
async def delete_conversations(
    ids: set[str] = Query(..., alias="id", min_length=1),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
):
    proxy_response = await application.delete_conversations(ids=list(ids))

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
