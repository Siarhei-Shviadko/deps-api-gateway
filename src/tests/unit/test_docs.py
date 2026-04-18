from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_PREFIX,
    BASE_API_V1_PREFIX,
    BASE_API_V5_PREFIX,
    SWAGGER_DOC_URL,
)


@pytest.mark.asyncio
async def test_get_v1_docs__ok(client: AsyncClient):
    response = await client.get(f"{BASE_API_V1_PREFIX}{SWAGGER_DOC_URL}")

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_v5_docs__ok(client: AsyncClient):
    response = await client.get(f"{BASE_API_V5_PREFIX}{SWAGGER_DOC_URL}")

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_v1_openapi__ok(client: AsyncClient):
    response = await client.get(f"{BASE_API_V1_PREFIX}/openapi.json")
    openapi_schema: dict[str, Any] = response.json()  # type: ignore

    assert response.status_code == HTTPStatus.OK
    assert all(key.startswith((BASE_API_V1_PREFIX, BASE_API_PREFIX)) for key in openapi_schema["paths"].keys())


@pytest.mark.asyncio
async def test_get_v5_openapi__ok(client: AsyncClient):
    response = await client.get(f"{BASE_API_V5_PREFIX}/openapi.json")
    openapi_schema: dict[str, Any] = response.json()  # type: ignore

    assert response.status_code == HTTPStatus.OK
    assert all(key.startswith(BASE_API_V5_PREFIX) for key in openapi_schema["paths"].keys())
