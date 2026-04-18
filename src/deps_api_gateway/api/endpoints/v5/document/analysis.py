from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentService
from deps_api_gateway.containers import Application

from ....serializers import (
    RetrieveFileInsightsRequest,
    RetrieveInsightsRequest,
    RetrieveInsightsResponse,
)
from ....utilities import ResponseBuilder

analysis_router = APIRouter(tags=["LLM Analysis"])


@analysis_router.post(
    "/documents/{documentId}/analysis/retrieve-insights",
    response_model=RetrieveInsightsResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def retrieve_insights(
    retrieve_insights_data: RetrieveInsightsRequest,
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.retrieve_insights(
        document_id=document_id,
        model=retrieve_insights_data.model,
        requested_insights=retrieve_insights_data.requested_insights_to_dict(),
        custom_instructions=retrieve_insights_data.custom_instructions,
        params=retrieve_insights_data.params.model_dump(),
        files=retrieve_insights_data.files,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@analysis_router.post(
    "/analysis/retrieve-file-insights",
    response_model=RetrieveInsightsResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def retrieve_file_insights(
    retrieve_insights_data: RetrieveFileInsightsRequest,
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.retrieve_file_insights(
        filepath=retrieve_insights_data.file_path,
        model=retrieve_insights_data.model,
        requested_insights=retrieve_insights_data.requested_insights_to_dict(),
        custom_instructions=retrieve_insights_data.custom_instructions,
        params=retrieve_insights_data.params.model_dump(),
        files=retrieve_insights_data.files,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
