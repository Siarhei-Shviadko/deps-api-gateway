from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import BuildOutputRequest, OutputsListResponse, SerializedOutput
from ....utilities import ResponseBuilder

__all__ = ["outputs_router"]

outputs_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Output Exporting"])


@outputs_router.get("/{documentId}/outputs", response_model=OutputsListResponse)
@inject
async def get_outputs(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_outputs(document_id=document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@outputs_router.post("/{documentId}/outputs", response_model=SerializedOutput)
@inject
async def build_output(
    output_data: BuildOutputRequest,
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.build_output(
        document_id=document_id,
        document_type_id=output_data.document_type_id,
        profile_id=output_data.profile_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@outputs_router.delete("/{documentId}/outputs/{outputId}", response_class=Response)
@inject
async def delete_output(
    document_id: str = Path(..., alias="documentId"),
    output_id: str = Path(..., alias="outputId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.delete_output(
        document_id=document_id,
        output_id=output_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
