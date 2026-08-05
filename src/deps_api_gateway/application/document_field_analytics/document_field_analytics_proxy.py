from datetime import datetime
from typing import Optional, Protocol

from ..proxy_response import ProxyResponse

__all__ = ["IDocumentFieldAnalyticsProxy"]


class IDocumentFieldAnalyticsProxy(Protocol):
    async def get_most_active_fields(
        self,
        limit: Optional[int],
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        pass

    async def get_most_missed_fields(
        self,
        limit: Optional[int],
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        pass

    async def get_field_analytics(
        self,
        document_id: str,
        field_code: str,
    ) -> ProxyResponse:
        pass

    async def get_all_analytics_for_field(
        self,
        field_code: str,
        document_type_id: str,
        page: Optional[int],
        per_page: Optional[int],
    ) -> ProxyResponse:
        pass

    async def get_field_quality_metrics(
        self,
        field_code: str,
        document_type_id: str,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        pass

    async def get_document_type_quality_metrics(
        self,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
    ) -> ProxyResponse:
        pass
