import asyncio
import json
import logging
from datetime import datetime
from http import HTTPStatus
from typing import Any, Optional

from ..iproxies import IExtraction
from ..proxy_response import ProxyResponse
from .consolidator import DocumentFieldAnalyticsConsolidator
from .document_field_analytics_proxy import IDocumentFieldAnalyticsProxy
from .inclusion_params import DocumentFieldAnalyticsExtras

__all__ = ["DocumentFieldAnalyticsService"]


class DocumentFieldAnalyticsService:
    def __init__(
        self,
        document_field_analytics_proxy: IDocumentFieldAnalyticsProxy,
        extraction_proxy: IExtraction,
    ) -> None:
        self._document_field_analytics_proxy = document_field_analytics_proxy
        self._extraction_proxy = extraction_proxy
        self._logger = logging.getLogger(__class__.__name__)

    async def get_most_active_fields(
        self,
        limit: Optional[int],
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        extras: Optional[list[DocumentFieldAnalyticsExtras]] = None,
    ) -> ProxyResponse:
        if not self._should_enrich_names(extras):
            return await self._document_field_analytics_proxy.get_most_active_fields(
                limit=limit,
                from_date=from_date,
                to_date=to_date,
            )

        analytics_response, extraction_data = await asyncio.gather(
            self._document_field_analytics_proxy.get_most_active_fields(
                limit=limit,
                from_date=from_date,
                to_date=to_date,
            ),
            self._safe_get_document_types(),
        )

        return DocumentFieldAnalyticsConsolidator.consolidate_most_active_fields(
            analytics_response=analytics_response,
            extraction_data=extraction_data,
        )

    async def get_most_missed_fields(
        self,
        limit: Optional[int],
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        extras: Optional[list[DocumentFieldAnalyticsExtras]] = None,
    ) -> ProxyResponse:
        if not self._should_enrich_names(extras):
            return await self._document_field_analytics_proxy.get_most_missed_fields(
                limit=limit,
                from_date=from_date,
                to_date=to_date,
            )

        analytics_response, extraction_data = await asyncio.gather(
            self._document_field_analytics_proxy.get_most_missed_fields(
                limit=limit,
                from_date=from_date,
                to_date=to_date,
            ),
            self._safe_get_document_types(),
        )

        return DocumentFieldAnalyticsConsolidator.consolidate_most_missed_fields(
            analytics_response=analytics_response,
            extraction_data=extraction_data,
        )

    async def get_field_analytics(
        self,
        document_id: str,
        field_code: str,
        extras: Optional[list[DocumentFieldAnalyticsExtras]] = None,
    ) -> ProxyResponse:
        if not self._should_enrich_names(extras):
            return await self._document_field_analytics_proxy.get_field_analytics(
                document_id=document_id,
                field_code=field_code,
            )

        analytics_response, extraction_data = await asyncio.gather(
            self._document_field_analytics_proxy.get_field_analytics(
                document_id=document_id,
                field_code=field_code,
            ),
            self._safe_get_document_types(),
        )

        return DocumentFieldAnalyticsConsolidator.consolidate_field_analytics(
            analytics_response=analytics_response,
            extraction_data=extraction_data,
        )

    async def get_all_analytics_for_field(
        self,
        field_code: str,
        document_type_id: str,
        page: Optional[int],
        per_page: Optional[int],
        extras: Optional[list[DocumentFieldAnalyticsExtras]] = None,
    ) -> ProxyResponse:
        if not self._should_enrich_names(extras):
            return await self._document_field_analytics_proxy.get_all_analytics_for_field(
                field_code=field_code,
                document_type_id=document_type_id,
                page=page,
                per_page=per_page,
            )

        analytics_response, extraction_data = await asyncio.gather(
            self._document_field_analytics_proxy.get_all_analytics_for_field(
                field_code=field_code,
                document_type_id=document_type_id,
                page=page,
                per_page=per_page,
            ),
            self._safe_get_document_type(document_type_id),
        )

        return DocumentFieldAnalyticsConsolidator.consolidate_all_analytics_for_field(
            analytics_response=analytics_response,
            extraction_data=extraction_data,
            document_type_id=document_type_id,
            field_code=field_code,
        )

    async def get_field_quality_metrics(
        self,
        field_code: str,
        document_type_id: str,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        extras: Optional[list[DocumentFieldAnalyticsExtras]] = None,
    ) -> ProxyResponse:
        if not self._should_enrich_names(extras):
            return await self._document_field_analytics_proxy.get_field_quality_metrics(
                field_code=field_code,
                document_type_id=document_type_id,
                from_date=from_date,
                to_date=to_date,
            )

        analytics_response, extraction_data = await asyncio.gather(
            self._document_field_analytics_proxy.get_field_quality_metrics(
                field_code=field_code,
                document_type_id=document_type_id,
                from_date=from_date,
                to_date=to_date,
            ),
            self._safe_get_document_type(document_type_id),
        )

        return DocumentFieldAnalyticsConsolidator.consolidate_field_quality_metrics(
            analytics_response=analytics_response,
            extraction_data=extraction_data,
        )

    async def get_document_type_quality_metrics(
        self,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        extras: Optional[list[DocumentFieldAnalyticsExtras]] = None,
    ) -> ProxyResponse:
        if not self._should_enrich_names(extras):
            return await self._document_field_analytics_proxy.get_document_type_quality_metrics(
                from_date=from_date,
                to_date=to_date,
            )

        analytics_response, extraction_data = await asyncio.gather(
            self._document_field_analytics_proxy.get_document_type_quality_metrics(
                from_date=from_date,
                to_date=to_date,
            ),
            self._safe_get_document_types(),
        )

        return DocumentFieldAnalyticsConsolidator.consolidate_document_type_quality_metrics(
            analytics_response=analytics_response,
            extraction_data=extraction_data,
        )

    @staticmethod
    def _should_enrich_names(extras: Optional[list[DocumentFieldAnalyticsExtras]]) -> bool:
        return extras is not None and DocumentFieldAnalyticsExtras.NAMES in extras

    async def _safe_get_document_types(self) -> Optional[dict[str, Any]]:
        try:
            response = await self._extraction_proxy.get_document_types()
            if response.get("status_code") != HTTPStatus.OK:
                self._logger.warning(
                    "Failed to fetch document types for analytics enrichment: status_code=%s",
                    response.get("status_code"),
                )
                return None
            return json.loads(response["content"])
        except Exception:
            self._logger.warning(
                "Failed to fetch document types for analytics enrichment",
                exc_info=True,
            )
            return None

    async def _safe_get_document_type(self, document_type_id: str) -> Optional[dict[str, Any]]:
        try:
            response = await self._extraction_proxy.get_document_type(document_type_id)
            if response.get("status_code") != HTTPStatus.OK:
                self._logger.warning(
                    "Failed to fetch document type %s for analytics enrichment: status_code=%s",
                    document_type_id,
                    response.get("status_code"),
                )
                return None
            return json.loads(response["content"])
        except Exception:
            self._logger.warning(
                "Failed to fetch document type %s for analytics enrichment",
                document_type_id,
                exc_info=True,
            )
            return None
