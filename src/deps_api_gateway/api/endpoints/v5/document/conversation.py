from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query, Response, status

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    CreateCompletionRequest,
    SerializedCompletion,
    SerializedConversationInfo,
)
from ....utilities import ResponseBuilder

__all__ = ["conversation_router"]

conversation_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Conversation"])


@conversation_router.put(
    "/{entityId}/conversation",
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedCompletion,
)
@inject
async def create_completion(
    entity_id: str = Path(..., alias="entityId"),
    completion: CreateCompletionRequest = Body(...),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.create_completion(
        entity_id=entity_id,
        provider=completion.provider,
        model=completion.model,
        question=completion.question,
        page_span=completion.page_span,
        files=completion.files,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversation_router.delete(
    "/{entityId}/conversation/completions",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def remove_completions(
    entity_id: str = Path(..., alias="entityId"),
    completion_codes: list[str] = Query(..., alias="completionCodes"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.remove_completions(entity_id=entity_id, completion_codes=completion_codes)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversation_router.get(
    "/{entityId}/conversation",
    response_model=SerializedConversationInfo,
)
@inject
async def get_conversation(
    entity_id: str = Path(..., alias="entityId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_conversation(entity_id=entity_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@conversation_router.delete(
    "/{entityId}/conversation",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def clear_conversation(
    entity_id: str = Path(..., alias="entityId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.clear_conversation(entity_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
