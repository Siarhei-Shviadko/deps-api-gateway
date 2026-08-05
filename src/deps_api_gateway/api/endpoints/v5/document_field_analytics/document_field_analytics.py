from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response, status

from deps_api_gateway.application import (
    DocumentFieldAnalyticsExtras,
    DocumentFieldAnalyticsService,
)
from deps_api_gateway.constants import DOCUMENT_FIELD_ANALYTICS_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    GetAllAnalyticsForFieldRequest,
    GetAllAnalyticsForFieldResponse,
    GetDocumentTypeQualityMetricsRequest,
    GetDocumentTypeQualityMetricsResponse,
    GetFieldAnalyticsRequest,
    GetFieldAnalyticsResponse,
    GetFieldQualityMetricsRequest,
    GetFieldQualityMetricsResponse,
    GetMostActiveFieldsRequest,
    GetMostActiveFieldsResponse,
    GetMostMissedFieldsRequest,
    GetMostMissedFieldsResponse,
)
from ....utilities import ResponseBuilder

__all__ = ["document_field_analytics_router"]

_NAMES_EXTRA_DESCRIPTION = (
    "Gateway-only. Use 'names' to enrich responses with document type and field names from extraction."
)

document_field_analytics_router = APIRouter(
    prefix=DOCUMENT_FIELD_ANALYTICS_ROUTER_PREFIX,
    tags=["Document Field Analytics"],
)


@document_field_analytics_router.get(
    "/most-active-fields",
    status_code=status.HTTP_200_OK,
    response_model=GetMostActiveFieldsResponse,
)
@inject
async def get_most_active_fields(
    request: GetMostActiveFieldsRequest = Depends(),
    extras: Optional[list[DocumentFieldAnalyticsExtras]] = Query(
        default=None,
        description=_NAMES_EXTRA_DESCRIPTION,
    ),
    document_field_analytics_service: DocumentFieldAnalyticsService = Depends(
        Provide[Application.document_field_analytics],
    ),
) -> Response:
    proxy_response = await document_field_analytics_service.get_most_active_fields(
        limit=request.limit,
        from_date=request.from_date,
        to_date=request.to_date,
        extras=extras,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_field_analytics_router.get(
    "/most-missed-fields",
    status_code=status.HTTP_200_OK,
    response_model=GetMostMissedFieldsResponse,
)
@inject
async def get_most_missed_fields(
    request: GetMostMissedFieldsRequest = Depends(),
    extras: Optional[list[DocumentFieldAnalyticsExtras]] = Query(
        default=None,
        description=_NAMES_EXTRA_DESCRIPTION,
    ),
    document_field_analytics_service: DocumentFieldAnalyticsService = Depends(
        Provide[Application.document_field_analytics],
    ),
) -> Response:
    proxy_response = await document_field_analytics_service.get_most_missed_fields(
        limit=request.limit,
        from_date=request.from_date,
        to_date=request.to_date,
        extras=extras,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_field_analytics_router.get(
    "/field-analytics",
    status_code=status.HTTP_200_OK,
    response_model=GetFieldAnalyticsResponse,
)
@inject
async def get_field_analytics(
    request: GetFieldAnalyticsRequest = Depends(),
    extras: Optional[list[DocumentFieldAnalyticsExtras]] = Query(
        default=None,
        description=_NAMES_EXTRA_DESCRIPTION,
    ),
    document_field_analytics_service: DocumentFieldAnalyticsService = Depends(
        Provide[Application.document_field_analytics],
    ),
) -> Response:
    proxy_response = await document_field_analytics_service.get_field_analytics(
        document_id=request.document_id,
        field_code=request.field_code,
        extras=extras,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_field_analytics_router.get(
    "/all-analytics-for-field",
    status_code=status.HTTP_200_OK,
    response_model=GetAllAnalyticsForFieldResponse,
)
@inject
async def get_all_analytics_for_field(
    request: GetAllAnalyticsForFieldRequest = Depends(),
    extras: Optional[list[DocumentFieldAnalyticsExtras]] = Query(
        default=None,
        description=_NAMES_EXTRA_DESCRIPTION,
    ),
    document_field_analytics_service: DocumentFieldAnalyticsService = Depends(
        Provide[Application.document_field_analytics],
    ),
) -> Response:
    proxy_response = await document_field_analytics_service.get_all_analytics_for_field(
        field_code=request.field_code,
        document_type_id=request.document_type_id,
        page=request.page,
        per_page=request.per_page,
        extras=extras,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_field_analytics_router.get(
    "/field-quality-metrics",
    status_code=status.HTTP_200_OK,
    response_model=GetFieldQualityMetricsResponse,
)
@inject
async def get_field_quality_metrics(
    request: GetFieldQualityMetricsRequest = Depends(),
    extras: Optional[list[DocumentFieldAnalyticsExtras]] = Query(
        default=None,
        description=_NAMES_EXTRA_DESCRIPTION,
    ),
    document_field_analytics_service: DocumentFieldAnalyticsService = Depends(
        Provide[Application.document_field_analytics],
    ),
) -> Response:
    proxy_response = await document_field_analytics_service.get_field_quality_metrics(
        field_code=request.field_code,
        document_type_id=request.document_type_id,
        from_date=request.from_date,
        to_date=request.to_date,
        extras=extras,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_field_analytics_router.get(
    "/document-type-quality-metrics",
    status_code=status.HTTP_200_OK,
    response_model=GetDocumentTypeQualityMetricsResponse,
)
@inject
async def get_document_type_quality_metrics(
    request: GetDocumentTypeQualityMetricsRequest = Depends(),
    extras: Optional[list[DocumentFieldAnalyticsExtras]] = Query(
        default=None,
        description=_NAMES_EXTRA_DESCRIPTION,
    ),
    document_field_analytics_service: DocumentFieldAnalyticsService = Depends(
        Provide[Application.document_field_analytics],
    ),
) -> Response:
    proxy_response = await document_field_analytics_service.get_document_type_quality_metrics(
        from_date=request.from_date,
        to_date=request.to_date,
        extras=extras,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
