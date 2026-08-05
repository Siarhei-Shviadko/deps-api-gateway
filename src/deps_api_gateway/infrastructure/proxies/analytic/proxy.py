from datetime import datetime
from typing import Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    IDocumentFieldAnalyticsProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import (
    ANALYTIC_BASE_API_PREFIX,
    DOCUMENT_FIELD_ANALYTICS_ROUTER_PREFIX,
    V1_PREFIX,
)

from ..generic_rest_client import GenericRestClient
from .exceptions import AnalyticServiceUnavailableError

__all__ = ["AnalyticProxy"]

_RESOURCE_PREFIX = f"{ANALYTIC_BASE_API_PREFIX}{V1_PREFIX}{DOCUMENT_FIELD_ANALYTICS_ROUTER_PREFIX}"


class AnalyticProxy(GenericRestClient, IDocumentFieldAnalyticsProxy):
    exception = AnalyticServiceUnavailableError
    RETRIED_STATUSES: set[int] = set()

    async def get_most_active_fields(
        self,
        limit: Optional[int],
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        params = _build_optional_params(
            limit=limit,
            from_date=from_date,
            to_date=to_date,
        )
        return await self._get(f"{_RESOURCE_PREFIX}/most-active-fields", params)

    async def get_most_missed_fields(
        self,
        limit: Optional[int],
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        params = _build_optional_params(
            limit=limit,
            from_date=from_date,
            to_date=to_date,
        )
        return await self._get(f"{_RESOURCE_PREFIX}/most-missed-fields", params)

    async def get_field_analytics(
        self,
        document_id: str,
        field_code: str,
    ) -> ProxyResponse:
        params = {
            "documentId": document_id,
            "fieldCode": field_code,
        }
        return await self._get(f"{_RESOURCE_PREFIX}/field-analytics", params)

    async def get_all_analytics_for_field(
        self,
        field_code: str,
        document_type_id: str,
        page: Optional[int],
        per_page: Optional[int],
    ) -> ProxyResponse:
        params: dict = {
            "fieldCode": field_code,
            "documentTypeId": document_type_id,
        }
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        return await self._get(f"{_RESOURCE_PREFIX}/all-analytics-for-field", params)

    async def get_field_quality_metrics(
        self,
        field_code: str,
        document_type_id: str,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        params = {
            "fieldCode": field_code,
            "documentTypeId": document_type_id,
        }
        if from_date is not None:
            params["fromDate"] = from_date.isoformat()
        if to_date is not None:
            params["toDate"] = to_date.isoformat()
        return await self._get(f"{_RESOURCE_PREFIX}/field-quality-metrics", params)

    async def get_document_type_quality_metrics(
        self,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        params = _build_optional_params(from_date=from_date, to_date=to_date)
        return await self._get(f"{_RESOURCE_PREFIX}/document-type-quality-metrics", params)

    async def _get(self, url: str, params: Optional[dict] = None) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=url, params=params or {}),
            )


def _build_optional_params(
    limit: Optional[int] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> dict:
    params: dict = {}
    if limit is not None:
        params["limit"] = limit
    if from_date is not None:
        params["fromDate"] = from_date.isoformat()
    if to_date is not None:
        params["toDate"] = to_date.isoformat()
    return params
