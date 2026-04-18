from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import AgenticAIService
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    CreateAgentVendorRequest,
    CreateAgentVendorResponse,
    GetAgentVendorsResponse,
)
from ....utilities import ResponseBuilder

__all__ = ["agent_vendors_router"]

agent_vendors_router = APIRouter(prefix="/agent-vendors", tags=["Agent Vendors"])


@agent_vendors_router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateAgentVendorResponse)
@inject
async def create_agent_vendor(
    agent_vendor: CreateAgentVendorRequest,
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.create_agent_vendor(
        name=agent_vendor.name,
        description=agent_vendor.description,
        base_url=agent_vendor.base_url,
        avatar_url=agent_vendor.avatar_url,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@agent_vendors_router.get("", status_code=status.HTTP_200_OK, response_model=GetAgentVendorsResponse)
@inject
async def get_agent_vendors(
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.get_agent_vendors()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@agent_vendors_router.patch("/{agentVendorId}/activate", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def activate_agent_vendor(
    agent_vendor_id: str = Path(..., alias="agentVendorId"),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.activate(agent_vendor_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@agent_vendors_router.delete("/{agentVendorId}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_agent_vendor(
    agent_vendor_id: str = Path(..., alias="agentVendorId"),
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.delete(agent_vendor_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
