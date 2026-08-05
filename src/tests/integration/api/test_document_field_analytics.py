import json
import urllib.parse
from http import HTTPStatus

import pytest
from aiohttp import ClientConnectionError
from aioresponses import aioresponses
from async_rest_client import Methods
from httpx import AsyncClient
from yarl import URL

from deps_api_gateway.constants import (
    ANALYTIC_BASE_API_PREFIX,
    BASE_API_V5_PREFIX,
    DOCUMENT_FIELD_ANALYTICS_ROUTER_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    V1_PREFIX,
)
from deps_api_gateway.infrastructure.proxies import AnalyticServiceUnavailableError
from tests.data.document_field_analytics_json_data import (
    ALL_ANALYTICS_FOR_FIELD_ENRICHED_RESPONSE,
    ALL_ANALYTICS_FOR_FIELD_LIST_VALUES_RESPONSE,
    ALL_ANALYTICS_FOR_FIELD_RESPONSE,
    ANALYTIC_NOT_FOUND_ERROR,
    DOCUMENT_TYPE_QUALITY_METRICS_ENRICHED_RESPONSE,
    DOCUMENT_TYPE_QUALITY_METRICS_RESPONSE,
    EXTRACTION_DOCUMENT_TYPE_INVOICE_RESPONSE,
    EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE,
    FIELD_ANALYTICS_ENRICHED_RESPONSE,
    FIELD_ANALYTICS_LIST_VALUES_RESPONSE,
    FIELD_ANALYTICS_RESPONSE,
    FIELD_QUALITY_METRICS_ENRICHED_RESPONSE,
    FIELD_QUALITY_METRICS_RESPONSE,
    MOST_ACTIVE_FIELDS_ENRICHED_RESPONSE,
    MOST_ACTIVE_FIELDS_RESPONSE,
    MOST_MISSED_FIELDS_ENRICHED_RESPONSE,
    MOST_MISSED_FIELDS_RESPONSE,
)

API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL = f"{BASE_API_V5_PREFIX}{DOCUMENT_FIELD_ANALYTICS_ROUTER_PREFIX}"
ANALYTIC_BASE_V1_URL = f"{ANALYTIC_BASE_API_PREFIX}{V1_PREFIX}{DOCUMENT_FIELD_ANALYTICS_ROUTER_PREFIX}"
EXTRACTION_DOCUMENT_TYPES_URL = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}/document-types"
EXTRACTION_DOCUMENT_TYPE_INVOICE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}/document-types/invoice"


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_most_active_fields__ok(client: AsyncClient):
    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/most-active-fields",
            status=HTTPStatus.OK,
            body=json.dumps(MOST_ACTIVE_FIELDS_RESPONSE),
        )

        response = await client.get(f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/most-active-fields")
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        assert response.json() == MOST_ACTIVE_FIELDS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_most_missed_fields__ok(client: AsyncClient):
    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/most-missed-fields",
            status=HTTPStatus.OK,
            body=json.dumps(MOST_MISSED_FIELDS_RESPONSE),
        )

        response = await client.get(f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/most-missed-fields")
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        assert response.json() == MOST_MISSED_FIELDS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_analytics__ok(client: AsyncClient):
    params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }
    backend_params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/field-analytics?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(FIELD_ANALYTICS_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-analytics",
            params=params,
        )
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIELD_ANALYTICS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_analytics__list_values__ok(client: AsyncClient):
    params = {
        "documentId": "doc-list-1",
        "fieldCode": "line_items",
    }
    backend_params = {
        "documentId": "doc-list-1",
        "fieldCode": "line_items",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/field-analytics?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(FIELD_ANALYTICS_LIST_VALUES_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-analytics",
            params=params,
        )
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body == FIELD_ANALYTICS_LIST_VALUES_RESPONSE
        assert isinstance(body["currentValue"], list)
        assert body["currentValue"] == [{"item": "A"}]
        assert body["modifications"][0]["oldValue"] == []
        assert body["modifications"][0]["newValue"] == [{"item": "A"}]


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_all_analytics_for_field__ok(client: AsyncClient):
    params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
        "page": 0,
        "perPage": 10,
    }
    backend_params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
        "page": 0,
        "perPage": 10,
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/all-analytics-for-field?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(ALL_ANALYTICS_FOR_FIELD_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/all-analytics-for-field",
            params=params,
        )
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        assert response.json() == ALL_ANALYTICS_FOR_FIELD_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_all_analytics_for_field__list_values__ok(client: AsyncClient):
    params = {
        "fieldCode": "line_items",
        "documentTypeId": "invoice",
    }
    backend_params = {
        "fieldCode": "line_items",
        "documentTypeId": "invoice",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/all-analytics-for-field?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(ALL_ANALYTICS_FOR_FIELD_LIST_VALUES_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/all-analytics-for-field",
            params=params,
        )
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body == ALL_ANALYTICS_FOR_FIELD_LIST_VALUES_RESPONSE
        assert isinstance(body["items"][0]["currentValue"], list)
        assert body["items"][0]["currentValue"] == [{"item": "A"}]


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_quality_metrics__ok(client: AsyncClient):
    params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
    }
    backend_params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/field-quality-metrics?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(FIELD_QUALITY_METRICS_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-quality-metrics",
            params=params,
        )
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIELD_QUALITY_METRICS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_document_type_quality_metrics__ok(client: AsyncClient):
    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/document-type-quality-metrics",
            status=HTTPStatus.OK,
            body=json.dumps(DOCUMENT_TYPE_QUALITY_METRICS_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/document-type-quality-metrics",
        )
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        assert response.json() == DOCUMENT_TYPE_QUALITY_METRICS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_analytics__not_found__passes_through(client: AsyncClient):
    params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }
    backend_params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }
    backend_url = f"{ANALYTIC_BASE_V1_URL}/field-analytics?{urllib.parse.urlencode(backend_params)}"

    with aioresponses() as mock_response:
        mock_response.get(
            backend_url,
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(ANALYTIC_NOT_FOUND_ERROR),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-analytics",
            params=params,
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == ANALYTIC_NOT_FOUND_ERROR


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_quality_metrics__not_found__passes_through(client: AsyncClient):
    params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
    }
    backend_params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
    }
    backend_url = f"{ANALYTIC_BASE_V1_URL}/field-quality-metrics?{urllib.parse.urlencode(backend_params)}"

    with aioresponses() as mock_response:
        mock_response.get(
            backend_url,
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(ANALYTIC_NOT_FOUND_ERROR),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-quality-metrics",
            params=params,
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == ANALYTIC_NOT_FOUND_ERROR


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_analytics__backend_error__passes_through(client: AsyncClient):
    params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }
    backend_params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }
    backend_url = f"{ANALYTIC_BASE_V1_URL}/field-analytics?{urllib.parse.urlencode(backend_params)}"
    error_body = {
        "code": "unhandled_error",
        "message": "Analytic service error",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            backend_url,
            status=HTTPStatus.BAD_GATEWAY,
            body=json.dumps(error_body),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-analytics",
            params=params,
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        assert response.json() == error_body


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_analytics__connection_error__service_unavailable(client: AsyncClient):
    params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }
    backend_params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }
    backend_url = f"{ANALYTIC_BASE_V1_URL}/field-analytics?{urllib.parse.urlencode(backend_params)}"

    with aioresponses() as mock_response:
        mock_response.get(
            backend_url,
            exception=ClientConnectionError("failed_connection"),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-analytics",
            params=params,
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        assert AnalyticServiceUnavailableError.code in response.content.decode()
        mock_response.assert_called_once()
        assert mock_response.requests.get((Methods.GET, URL(backend_url)))


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_most_active_fields__with_names_extra__ok(client: AsyncClient):
    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/most-active-fields",
            status=HTTPStatus.OK,
            body=json.dumps(MOST_ACTIVE_FIELDS_RESPONSE),
        )
        mock_response.get(
            EXTRACTION_DOCUMENT_TYPES_URL,
            status=HTTPStatus.OK,
            body=json.dumps(EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/most-active-fields",
            params={"extras": "names"},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == MOST_ACTIVE_FIELDS_ENRICHED_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_most_missed_fields__with_names_extra__ok(client: AsyncClient):
    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/most-missed-fields",
            status=HTTPStatus.OK,
            body=json.dumps(MOST_MISSED_FIELDS_RESPONSE),
        )
        mock_response.get(
            EXTRACTION_DOCUMENT_TYPES_URL,
            status=HTTPStatus.OK,
            body=json.dumps(EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/most-missed-fields",
            params={"extras": "names"},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == MOST_MISSED_FIELDS_ENRICHED_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_analytics__with_names_extra__ok(client: AsyncClient):
    params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
        "extras": "names",
    }
    backend_params = {
        "documentId": "doc-1",
        "fieldCode": "invoice_number",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/field-analytics?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(FIELD_ANALYTICS_RESPONSE),
        )
        mock_response.get(
            EXTRACTION_DOCUMENT_TYPES_URL,
            status=HTTPStatus.OK,
            body=json.dumps(EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-analytics",
            params=params,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIELD_ANALYTICS_ENRICHED_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_all_analytics_for_field__with_names_extra__ok(client: AsyncClient):
    params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
        "page": 0,
        "perPage": 10,
        "extras": "names",
    }
    backend_params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
        "page": 0,
        "perPage": 10,
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/all-analytics-for-field?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(ALL_ANALYTICS_FOR_FIELD_RESPONSE),
        )
        mock_response.get(
            EXTRACTION_DOCUMENT_TYPE_INVOICE_URL,
            status=HTTPStatus.OK,
            body=json.dumps(EXTRACTION_DOCUMENT_TYPE_INVOICE_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/all-analytics-for-field",
            params=params,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == ALL_ANALYTICS_FOR_FIELD_ENRICHED_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_field_quality_metrics__with_names_extra__ok(client: AsyncClient):
    params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
        "extras": "names",
    }
    backend_params = {
        "fieldCode": "invoice_number",
        "documentTypeId": "invoice",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/field-quality-metrics?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(FIELD_QUALITY_METRICS_RESPONSE),
        )
        mock_response.get(
            EXTRACTION_DOCUMENT_TYPE_INVOICE_URL,
            status=HTTPStatus.OK,
            body=json.dumps(EXTRACTION_DOCUMENT_TYPE_INVOICE_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/field-quality-metrics",
            params=params,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIELD_QUALITY_METRICS_ENRICHED_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_document_type_quality_metrics__with_names_extra__ok(client: AsyncClient):
    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/document-type-quality-metrics",
            status=HTTPStatus.OK,
            body=json.dumps(DOCUMENT_TYPE_QUALITY_METRICS_RESPONSE),
        )
        mock_response.get(
            EXTRACTION_DOCUMENT_TYPES_URL,
            status=HTTPStatus.OK,
            body=json.dumps(EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE),
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/document-type-quality-metrics",
            params={"extras": "names"},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == DOCUMENT_TYPE_QUALITY_METRICS_ENRICHED_RESPONSE


@pytest.mark.asyncio
@pytest.mark.document_field_analytics
async def test_get_most_active_fields__with_names_extra__extraction_unavailable__returns_analytics(
    client: AsyncClient,
):
    with aioresponses() as mock_response:
        mock_response.get(
            f"{ANALYTIC_BASE_V1_URL}/most-active-fields",
            status=HTTPStatus.OK,
            body=json.dumps(MOST_ACTIVE_FIELDS_RESPONSE),
        )
        mock_response.get(
            EXTRACTION_DOCUMENT_TYPES_URL,
            status=HTTPStatus.SERVICE_UNAVAILABLE,
        )

        response = await client.get(
            f"{API_GATEWAY_DOCUMENT_FIELD_ANALYTICS_V5_URL}/most-active-fields",
            params={"extras": "names"},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == MOST_ACTIVE_FIELDS_RESPONSE
