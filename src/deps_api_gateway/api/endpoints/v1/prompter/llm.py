from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from deps_api_gateway.application.legacy import PrompterService
from deps_api_gateway.containers import Application

from ....utilities import ResponseBuilder

__all__ = ["prompter_router"]

prompter_router = APIRouter(prefix="/prompter", tags=["LLMs"])


@prompter_router.get(
    "/models",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
@inject
async def get_llms_with_codes(
    prompter_service: PrompterService = Depends(Provide[Application.prompter]),
):
    response = await prompter_service.get_llms_with_codes()
    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )
