import json
from http import HTTPStatus

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    META_AGENT_BASE_API_PREFIX,
    V1_PREFIX,
)

META_AGENT_BASE_URL = f"{META_AGENT_BASE_API_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
async def test_register_manifest__201_status(client: AsyncClient):
    url = f"{META_AGENT_BASE_URL}/manifests"
    payload = {
        "code": "manifest_code",
        "name": "manifest name",
        "description": "manfest description",
        "url": "asd.com",
        "timeout": 1,
    }
    expected_response = {"code": "manifest_code"}

    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.CREATED, body=json.dumps(expected_response))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/agentic-ai/manifests",
            json=payload,
        )

        assert response.status_code == HTTPStatus.CREATED
        mock_response.assert_called_once()
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_meta_agent__service_unavailable__502_status(client: AsyncClient):
    url = f"{META_AGENT_BASE_URL}/manifests"
    payload = {
        "code": "manifest_code",
        "name": "manifest name",
        "description": "manfest description",
        "url": "asd.com",
        "timeout": 1,
    }

    with aioresponses() as mock_response:
        mock_response.post(url, exception=ClientConnectionError("failed_connection"))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/agentic-ai/manifests",
            json=payload,
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
async def test_delete_manifests__204_status(client: AsyncClient):
    url = f"{META_AGENT_BASE_URL}/manifests?code=code1&code=code2"

    with aioresponses() as mock_response:
        mock_response.delete(url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(
            f"{BASE_API_V5_PREFIX}/agentic-ai/manifests?code=code1&code=code2",
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_response.assert_called_once()


@pytest.mark.asyncio
async def test_delete_manifests__service_unavailable__502_status(client: AsyncClient):
    url = f"{META_AGENT_BASE_URL}/manifests?code=code1"

    with aioresponses() as mock_response:
        mock_response.delete(url, exception=ClientConnectionError("failed_connection"))

        response = await client.delete(
            f"{BASE_API_V5_PREFIX}/agentic-ai/manifests?code=code1",
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
async def test_delete_manifests__large_batch__204_status(client: AsyncClient):
    codes = [f"code{i}" for i in range(1, 11)]
    query_params = "&".join([f"code={code}" for code in codes])
    url = f"{META_AGENT_BASE_URL}/manifests?{query_params}"

    with aioresponses() as mock_response:
        mock_response.delete(url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(
            f"{BASE_API_V5_PREFIX}/agentic-ai/manifests?{query_params}",
        )
        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_manifests__empty_list__422_status(client: AsyncClient):
    response = await client.delete(
        f"{BASE_API_V5_PREFIX}/agentic-ai/manifests",
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
