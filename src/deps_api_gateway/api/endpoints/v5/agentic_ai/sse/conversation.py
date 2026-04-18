import json
import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import StreamingResponse

from deps_api_gateway.application import AgenticAIService
from deps_api_gateway.containers import Application
from deps_api_gateway.domain.exceptions import IllegalArgument
from deps_api_gateway.infrastructure import AgenticAIServiceUnavailableError

from .....serializers.v5 import ChatRequest

logger = logging.getLogger(__name__)

__all__ = ["sse_conversations_router"]

sse_conversations_router = APIRouter(prefix="/conversations", tags=["Conversations"])


@sse_conversations_router.get(
    "/{conversationId}/chat",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    description="Stream chat messages for a conversation using Server-Sent Events",
)
@inject
async def chat(
    request: ChatRequest = Depends(ChatRequest.from_query_params),
    conversation_id: str = Path(..., alias="conversationId"),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> StreamingResponse:
    async def event_generator():  # noqa: WPS430
        chat_stream = None
        try:
            chat_stream = application.chat(
                conversation_id=conversation_id,
                user_question=request.user_question,
                arguments=request.to_context_arguments(),
            )

            async for chunk in chat_stream:
                yield chunk

        except Exception as e:
            if isinstance(e, (IllegalArgument, AgenticAIServiceUnavailableError)):
                error_message = str(e)
            else:
                error_message = "An unexpected error occurred"
            logger.exception("SSE streaming error: %s", e, exc_info=True)

            data = json.dumps({"type": "Error", "text": error_message})
            yield f"event: error\ndata: {data}\n\n".encode()

        finally:
            if chat_stream is not None and hasattr(chat_stream, "aclose"):
                await chat_stream.aclose()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx's response buffering
        },
    )


@sse_conversations_router.patch(
    "/{conversationId}/completions/{completionId}",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    description="Stream chat messages for a conversation after editing question using Server-Sent Events",
)
@inject
async def edit_question(
    request: ChatRequest = Depends(ChatRequest.from_query_params),
    conversation_id: str = Path(..., alias="conversationId"),
    completion_id: str = Path(..., alias="completionId"),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> StreamingResponse:
    async def event_generator():  # noqa: WPS430
        chat_stream = None
        try:
            chat_stream = application.edit_question(
                conversation_id=conversation_id,
                completion_id=completion_id,
                user_question=request.user_question,
                arguments=request.to_context_arguments(),
            )

            async for chunk in chat_stream:
                yield chunk

        except Exception as e:
            if isinstance(e, (IllegalArgument, AgenticAIServiceUnavailableError)):
                error_message = str(e)
            else:
                error_message = "An unexpected error occurred"
            logger.exception("SSE streaming error: %s", e, exc_info=True)

            data = json.dumps({"type": "Error", "text": error_message})
            yield f"event: error\ndata: {data}\n\n".encode()

        finally:
            if chat_stream is not None and hasattr(chat_stream, "aclose"):
                await chat_stream.aclose()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx's response buffering
        },
    )
