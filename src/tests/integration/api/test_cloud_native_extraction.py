from http import HTTPStatus

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    CLOUD_NATIVE_BASE_API_PREFIX,
    DOCUMENT_TYPE_ROUTER_PREFIX,
)
from tests.data.cloud_native_json_data import (
    AZURE_EXTRACTOR_HEALTHCHECK_DICT,
    AZURE_EXTRACTOR_HEALTHCHECK_JSON,
    AZURE_EXTRACTOR_INFO_DICT,
    AZURE_EXTRACTOR_INFO_JSON,
)


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "test-name", "modelId": "test-model-id", "endpoint": "test-endpoint", "apiKey": "test-api-key"},
        {
            "name": "test-name",
            "modelId": "test-model-id",
            "endpoint": "test-endpoint",
            "apiKey": "test-api-key",
            "language": "english",
            "description": "HelloCloud",
        },
    ],
)
@pytest.mark.asyncio
async def test_create_azure_extractor__ok(payload, client):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_TYPE_ROUTER_PREFIX}/azure-extractor"
    cloud_native_url = f"{CLOUD_NATIVE_BASE_API_PREFIX}/v1/azure/extractor"
    document_type_id = "fake_document_type_id"

    with aioresponses() as mock_response:
        mock_response.post(cloud_native_url, body=document_type_id, status=HTTPStatus.CREATED)

        response = await client.post(url, json=payload)
        sended_payload = [resp[0] for resp in mock_response.requests.values()][0].kwargs["json"]
        expected_payload = {k: v for k, v in sended_payload.items() if v is not None}

        assert response.status_code == HTTPStatus.CREATED
        assert response.text == document_type_id
        mock_response.assert_called_once()
        assert expected_payload == payload


@pytest.mark.asyncio
async def test_cloud_native_extraction__service_unavailable__502_error(client, document_id):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_TYPE_ROUTER_PREFIX}/azure-extractor"
    cloud_native_url = f"{CLOUD_NATIVE_BASE_API_PREFIX}/v1/azure/extractor"
    data = {"name": "test-name", "modelId": "test-model-id", "endpoint": "test-endpoint", "apiKey": "test-api-key"}

    with aioresponses() as mock_response:
        mock_response.post(cloud_native_url, exception=ClientConnectionError("failed_connection"))

        response = await client.post(url, json=data)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
async def test_get_azure_extractor_info__ok(client):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_TYPE_ROUTER_PREFIX}/NiceId/azure-extractor"
    cloud_native_url = f"{CLOUD_NATIVE_BASE_API_PREFIX}/v1/azure/extractor/NiceId"

    with aioresponses() as mock_response:
        mock_response.get(cloud_native_url, body=AZURE_EXTRACTOR_INFO_JSON, status=HTTPStatus.OK)

        response = await client.get(url)

        assert response.status_code == HTTPStatus.OK

        mock_response.assert_called_once()
        assert response.json() == AZURE_EXTRACTOR_INFO_DICT


@pytest.mark.asyncio
async def test_validate_azure_credentials__ok(client):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_TYPE_ROUTER_PREFIX}/azure-extractor/validate-credentials"
    cloud_native_url = f"{CLOUD_NATIVE_BASE_API_PREFIX}/v1/azure/validate-credentials"

    with aioresponses() as mock_response:
        mock_response.post(cloud_native_url, status=HTTPStatus.OK)
        data = {"endpoint": "my_endpoint", "modelId": "my_model_id", "apiKey": "my_api_key"}
        response = await client.post(url, json=data)

        assert response.status_code == HTTPStatus.OK

        mock_response.assert_called_once()


@pytest.mark.asyncio
async def test_update_azure_extractor__ok(client, document_type_id: str):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_TYPE_ROUTER_PREFIX}/{document_type_id}/azure-extractor"
    cloud_native_url = f"{CLOUD_NATIVE_BASE_API_PREFIX}/v1/azure/extractor/{document_type_id}"
    data = {
        "modelId": "model_id",
        "endpoint": "endpoint",
        "apiKey": "api_key",
    }

    with aioresponses() as mock_response:
        mock_response.put(cloud_native_url, status=HTTPStatus.NO_CONTENT)
        response = await client.put(url, json=data)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_azure_extractor_healthcheck__ok(client):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_TYPE_ROUTER_PREFIX}/NiceId/azure-extractor/checkup"
    cloud_native_url = f"{CLOUD_NATIVE_BASE_API_PREFIX}/v1/azure/extractor/NiceId/checkup"

    with aioresponses() as mock_response:
        mock_response.get(cloud_native_url, body=AZURE_EXTRACTOR_HEALTHCHECK_JSON, status=HTTPStatus.OK)

        response = await client.get(url)

        assert response.status_code == HTTPStatus.OK

        mock_response.assert_called_once()
        assert response.json() == AZURE_EXTRACTOR_HEALTHCHECK_DICT


@pytest.mark.asyncio
async def test_synchronize_azure_extractor__ok(client):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_TYPE_ROUTER_PREFIX}/NiceId/azure-extractor/synchronize"
    cloud_native_url = f"{CLOUD_NATIVE_BASE_API_PREFIX}/v1/azure/extractor/NiceId/synchronize"

    with aioresponses() as mock_response:
        mock_response.put(cloud_native_url, status=HTTPStatus.OK)

        response = await client.put(url)

        assert response.status_code == HTTPStatus.OK

        mock_response.assert_called_once()
