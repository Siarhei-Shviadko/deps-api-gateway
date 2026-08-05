from dataclasses import dataclass
from typing import Any, Optional

from ..proxy_response import ProxyResponse

__all__ = ["DocumentFieldAnalyticsConsolidator"]


@dataclass(frozen=True)
class _DocumentFieldAnalyticsLookup:
    document_type_names: dict[str, str]
    field_names: dict[tuple[str, str], str]


class DocumentFieldAnalyticsConsolidator:
    @classmethod
    def consolidate_most_active_fields(
        cls,
        analytics_response: ProxyResponse,
        extraction_data: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        return cls._consolidate_items_response(analytics_response, extraction_data)

    @classmethod
    def consolidate_most_missed_fields(
        cls,
        analytics_response: ProxyResponse,
        extraction_data: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        return cls._consolidate_items_response(analytics_response, extraction_data)

    @classmethod
    def consolidate_document_type_quality_metrics(
        cls,
        analytics_response: ProxyResponse,
        extraction_data: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        if not analytics_response.is_ok() or extraction_data is None:
            return analytics_response

        lookup = cls._build_lookup_from_document_types_list(extraction_data)
        content: dict[str, Any] = analytics_response.json()  # type: ignore

        for analytics_entry in content["items"]:
            cls._enrich_names_on_content(
                content=analytics_entry,
                lookup=lookup,
                document_type_id=analytics_entry.get("documentTypeId"),
                field_code=None,
            )

        return analytics_response.with_updated_content(
            status_code=analytics_response.status_code,
            content=content,
            headers=analytics_response.headers,
        )

    @classmethod
    def consolidate_field_analytics(
        cls,
        analytics_response: ProxyResponse,
        extraction_data: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        if not analytics_response.is_ok() or extraction_data is None:
            return analytics_response

        lookup = cls._build_lookup_from_document_types_list(extraction_data)
        content: dict[str, Any] = analytics_response.json()  # type: ignore
        cls._enrich_root(content, lookup)

        return analytics_response.with_updated_content(
            status_code=analytics_response.status_code,
            content=content,
            headers=analytics_response.headers,
        )

    @classmethod
    def consolidate_field_quality_metrics(
        cls,
        analytics_response: ProxyResponse,
        extraction_data: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        if not analytics_response.is_ok() or extraction_data is None:
            return analytics_response

        lookup = cls._build_lookup_from_single_document_type(extraction_data)
        content: dict[str, Any] = analytics_response.json()  # type: ignore
        cls._enrich_root(content, lookup)

        return analytics_response.with_updated_content(
            status_code=analytics_response.status_code,
            content=content,
            headers=analytics_response.headers,
        )

    @classmethod
    def consolidate_all_analytics_for_field(
        cls,
        analytics_response: ProxyResponse,
        extraction_data: Optional[dict[str, Any]],
        document_type_id: str,
        field_code: str,
    ) -> ProxyResponse:
        if not analytics_response.is_ok() or extraction_data is None:
            return analytics_response

        lookup = cls._build_lookup_from_single_document_type(extraction_data)
        content: dict[str, Any] = analytics_response.json()  # type: ignore
        cls._enrich_names_on_content(
            content=content,
            lookup=lookup,
            document_type_id=document_type_id,
            field_code=field_code,
        )

        for analytics_entry in content["items"]:
            cls._enrich_names_on_content(
                content=analytics_entry,
                lookup=lookup,
                document_type_id=document_type_id,
                field_code=field_code,
            )

        return analytics_response.with_updated_content(
            status_code=analytics_response.status_code,
            content=content,
            headers=analytics_response.headers,
        )

    @classmethod
    def _consolidate_items_response(
        cls,
        analytics_response: ProxyResponse,
        extraction_data: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        if not analytics_response.is_ok() or extraction_data is None:
            return analytics_response

        lookup = cls._build_lookup_from_document_types_list(extraction_data)
        content: dict[str, Any] = analytics_response.json()  # type: ignore

        for analytics_entry in content["items"]:
            cls._enrich_item(analytics_entry, lookup)

        return analytics_response.with_updated_content(
            status_code=analytics_response.status_code,
            content=content,
            headers=analytics_response.headers,
        )

    @classmethod
    def _build_lookup_from_document_types_list(cls, extraction_data: dict[str, Any]) -> _DocumentFieldAnalyticsLookup:
        document_type_names: dict[str, str] = {}
        field_names: dict[tuple[str, str], str] = {}

        for document_type in extraction_data.get("result", []):
            document_type_id = document_type["id"]
            document_type_names[document_type_id] = document_type["documentType"]
            for field in document_type.get("fields", []):
                field_names[(document_type_id, field["code"])] = field["name"]

        return _DocumentFieldAnalyticsLookup(
            document_type_names=document_type_names,
            field_names=field_names,
        )

    @classmethod
    def _build_lookup_from_single_document_type(cls, extraction_data: dict[str, Any]) -> _DocumentFieldAnalyticsLookup:
        document_type_id = extraction_data["id"]
        document_type_names = {document_type_id: extraction_data["documentType"]}
        field_names: dict[tuple[str, str], str] = {}
        for field in extraction_data.get("fields", []):
            field_names[(document_type_id, field["code"])] = field["name"]

        return _DocumentFieldAnalyticsLookup(
            document_type_names=document_type_names,
            field_names=field_names,
        )

    @classmethod
    def _enrich_item(cls, analytics_entry: dict[str, Any], lookup: _DocumentFieldAnalyticsLookup) -> None:
        document_type_id = analytics_entry.get("documentTypeId")
        field_code = analytics_entry.get("fieldCode")
        cls._enrich_names_on_content(
            content=analytics_entry,
            lookup=lookup,
            document_type_id=document_type_id,
            field_code=field_code,
        )

    @classmethod
    def _enrich_root(cls, content: dict[str, Any], lookup: _DocumentFieldAnalyticsLookup) -> None:
        cls._enrich_names_on_content(
            content=content,
            lookup=lookup,
            document_type_id=content.get("documentTypeId"),
            field_code=content.get("fieldCode"),
        )

    @classmethod
    def _enrich_names_on_content(
        cls,
        content: dict[str, Any],
        lookup: _DocumentFieldAnalyticsLookup,
        document_type_id: Optional[str],
        field_code: Optional[str],
    ) -> None:
        if document_type_id is not None:
            document_type_name = lookup.document_type_names.get(document_type_id)
            if document_type_name is not None:
                content["documentTypeName"] = document_type_name

        if document_type_id is not None and field_code is not None:
            field_name = lookup.field_names.get((document_type_id, field_code))
            if field_name is not None:
                content["fieldName"] = field_name
