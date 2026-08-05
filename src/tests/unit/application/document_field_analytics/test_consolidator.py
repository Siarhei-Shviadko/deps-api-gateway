from deps_api_gateway.application.document_field_analytics import (
    DocumentFieldAnalyticsConsolidator,
)
from tests.data.document_field_analytics_json_data import (
    ALL_ANALYTICS_FOR_FIELD_ENRICHED_RESPONSE,
    ALL_ANALYTICS_FOR_FIELD_RESPONSE,
    DOCUMENT_TYPE_QUALITY_METRICS_ENRICHED_RESPONSE,
    DOCUMENT_TYPE_QUALITY_METRICS_RESPONSE,
    EXTRACTION_DOCUMENT_TYPE_INVOICE_RESPONSE,
    EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE,
    FIELD_ANALYTICS_ENRICHED_RESPONSE,
    FIELD_ANALYTICS_RESPONSE,
    FIELD_QUALITY_METRICS_ENRICHED_RESPONSE,
    FIELD_QUALITY_METRICS_RESPONSE,
    MOST_ACTIVE_FIELDS_ENRICHED_RESPONSE,
    MOST_ACTIVE_FIELDS_RESPONSE,
    MOST_MISSED_FIELDS_ENRICHED_RESPONSE,
    MOST_MISSED_FIELDS_RESPONSE,
)


def test_consolidate_most_active_fields__enriches_names(ok_proxy_response__maker) -> None:
    analytics_response = ok_proxy_response__maker(MOST_ACTIVE_FIELDS_RESPONSE)

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_most_active_fields(
        analytics_response=analytics_response,
        extraction_data=EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE,
    )

    assert consolidated.json() == MOST_ACTIVE_FIELDS_ENRICHED_RESPONSE


def test_consolidate_most_missed_fields__enriches_names(ok_proxy_response__maker) -> None:
    analytics_response = ok_proxy_response__maker(MOST_MISSED_FIELDS_RESPONSE)

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_most_missed_fields(
        analytics_response=analytics_response,
        extraction_data=EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE,
    )

    assert consolidated.json() == MOST_MISSED_FIELDS_ENRICHED_RESPONSE


def test_consolidate_field_analytics__enriches_names(ok_proxy_response__maker) -> None:
    analytics_response = ok_proxy_response__maker(FIELD_ANALYTICS_RESPONSE)

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_field_analytics(
        analytics_response=analytics_response,
        extraction_data=EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE,
    )

    assert consolidated.json() == FIELD_ANALYTICS_ENRICHED_RESPONSE


def test_consolidate_all_analytics_for_field__enriches_names_on_root_and_items(ok_proxy_response__maker) -> None:
    analytics_response = ok_proxy_response__maker(ALL_ANALYTICS_FOR_FIELD_RESPONSE)

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_all_analytics_for_field(
        analytics_response=analytics_response,
        extraction_data=EXTRACTION_DOCUMENT_TYPE_INVOICE_RESPONSE,
        document_type_id="invoice",
        field_code="invoice_number",
    )

    assert consolidated.json() == ALL_ANALYTICS_FOR_FIELD_ENRICHED_RESPONSE


def test_consolidate_field_quality_metrics__enriches_names(ok_proxy_response__maker) -> None:
    analytics_response = ok_proxy_response__maker(FIELD_QUALITY_METRICS_RESPONSE)

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_field_quality_metrics(
        analytics_response=analytics_response,
        extraction_data=EXTRACTION_DOCUMENT_TYPE_INVOICE_RESPONSE,
    )

    assert consolidated.json() == FIELD_QUALITY_METRICS_ENRICHED_RESPONSE


def test_consolidate_document_type_quality_metrics__enriches_names(ok_proxy_response__maker) -> None:
    analytics_response = ok_proxy_response__maker(DOCUMENT_TYPE_QUALITY_METRICS_RESPONSE)

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_document_type_quality_metrics(
        analytics_response=analytics_response,
        extraction_data=EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE,
    )

    assert consolidated.json() == DOCUMENT_TYPE_QUALITY_METRICS_ENRICHED_RESPONSE


def test_consolidate_most_active_fields__unknown_lookup__names_omitted(ok_proxy_response__maker) -> None:
    analytics_response = ok_proxy_response__maker(MOST_ACTIVE_FIELDS_RESPONSE)
    extraction_data = {
        "result": [
            {
                "id": "other-type",
                "documentType": "Other",
                "fields": [{"code": "other_field", "name": "Other Field"}],
            },
        ],
    }

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_most_active_fields(
        analytics_response=analytics_response,
        extraction_data=extraction_data,
    )

    assert consolidated.json() == MOST_ACTIVE_FIELDS_RESPONSE


def test_consolidate_most_active_fields__extraction_unavailable__analytics_unchanged(
    ok_proxy_response__maker,
) -> None:
    analytics_response = ok_proxy_response__maker(MOST_ACTIVE_FIELDS_RESPONSE)

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_most_active_fields(
        analytics_response=analytics_response,
        extraction_data=None,
    )

    assert consolidated.json() == MOST_ACTIVE_FIELDS_RESPONSE


def test_consolidate_most_active_fields__analytics_not_ok__returned_as_is(not_ok_proxy_response__maker) -> None:
    analytics_response = not_ok_proxy_response__maker(
        status_code=400,
        data=MOST_ACTIVE_FIELDS_RESPONSE,
    )

    consolidated = DocumentFieldAnalyticsConsolidator.consolidate_most_active_fields(
        analytics_response=analytics_response,
        extraction_data=EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE,
    )

    assert consolidated == analytics_response
