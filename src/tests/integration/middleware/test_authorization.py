import asyncio
import json
from http import HTTPStatus
from typing import AsyncGenerator
from unittest.mock import patch

import pytest
import pytest_asyncio
from fastapi import FastAPI, Response
from httpx import ASGITransport, AsyncClient

from deps_api_gateway.constants import CORLEONE_BASE_API_PREFIX, V1_PREFIX
from deps_api_gateway.entrypoint import create_fastapi
from deps_api_gateway.middleware.authorization import AuthorizationMiddleware
from tests.data.json_data import (
    TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
    TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
)

CORLEONE_URL = f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}"
HEADERS = {
    "deps-token": '{"email": "user@test.com", "first_name": "Name", "last_name": "Surname", "roles": [], "groups": [], "subject": "subject", "organisation": "deps-users"}'
}
GENERIC_REST_CLIENT_PATH = (
    "deps_api_gateway.infrastructure.proxies.generic_rest_client.old.OldGenericRestClient.request"
)
AUTHORIZATION_REQUEST_PATH = "deps_api_gateway.middleware.authorization.AuthorizationMiddleware._authorize"


@pytest.fixture()
def mocked_document_type_request(mocker):
    mock = [
        {
            "content": TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=mock)
    return mock


@pytest.fixture()
def mocked_document_types_request(mocker):
    mock = [
        {
            "content": TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=mock)
    return mock


@pytest_asyncio.fixture(scope="class")
async def app() -> AsyncGenerator:
    fastapi_app = create_fastapi()
    yield fastapi_app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.fixture(scope="class")
def containers(app):
    yield app.containers


@pytest.fixture(scope="class")
def authorization_middleware(app):
    middleware = app.add_middleware(AuthorizationMiddleware, iam_url="http://deps-iam-api:8000")
    yield middleware


@pytest.mark.asyncio
@patch(AUTHORIZATION_REQUEST_PATH)
class TestAuthorizationMiddleware:
    async def test_route_request__successful_authorization__success(
        self,
        authorization_mock,
        app,
        client,
        mocked_document_type_request,
        document_type_source_cache,
        authorization_middleware,
    ):
        document_type_source_cache.clear()

        authorization_mock.return_value = Response(status_code=200, headers=HEADERS)
        res = await client.get(f"{CORLEONE_URL}/types/111", headers=HEADERS)
        authorization_mock.assert_called()
        assert res.status_code == HTTPStatus.OK

    async def test_route_request__failed_authorization__error(
        self,
        authorization_mock,
        app,
        client,
        mocked_document_type_request,
        document_type_source_cache,
        authorization_middleware,
    ):
        document_type_source_cache.clear()

        authorization_mock.return_value = Response(status_code=400, headers=HEADERS)

        res = await client.get(f"{CORLEONE_URL}/types/111", headers=HEADERS)

        authorization_mock.assert_called()
        assert res.status_code == HTTPStatus.UNAUTHORIZED

    async def test_route_docs_request__skipped_authorization__success(
        self,
        authorization_mock,
        app,
        client,
        mocked_document_type_request,
        document_type_source_cache,
        authorization_middleware,
    ):
        document_type_source_cache.clear()

        res = await client.get(f"{CORLEONE_URL}/docs", headers=HEADERS)

        authorization_mock.assert_not_called()
        assert res.status_code == HTTPStatus.OK

    async def test_route_request__pass_path_to_authorization_service(
        self,
        authorization_mock,
        app,
        client,
        mocked_document_type_request,
        document_type_source_cache,
        authorization_middleware,
    ):
        document_type_source_cache.clear()

        authorization_mock.return_value = Response(status_code=200, headers=HEADERS)

        res = await client.get(f"{CORLEONE_URL}/types/111", headers=HEADERS)

        assert res.status_code == HTTPStatus.OK
        assert ("x-original-path", "/api/corleone/v1/types/111") in authorization_mock.call_args[1]["headers"].items()

    async def test_route_request__pass_query_params_to_authorization_service(
        self,
        authorization_mock,
        app,
        client,
        mocked_document_types_request,
        document_type_source_cache,
        authorization_middleware,
    ):
        document_type_source_cache.clear()

        authorization_mock.return_value = Response(status_code=200, headers=HEADERS)

        res = await client.get(f"{CORLEONE_URL}/types?name=111", headers=HEADERS)

        assert res.status_code == HTTPStatus.OK
        assert ("x-original-query", b"name=111") in authorization_mock.call_args[1]["headers"].items()

    async def test_route_request__pass_body_to_authorization_service(
        self,
        authorization_mock,
        app,
        client,
        mocked_document_type_request,
        document_type_source_cache,
        authorization_middleware,
    ):
        document_type_source_cache.clear()

        authorization_mock.return_value = Response(status_code=200, headers=HEADERS)

        res = await client.post(f"{CORLEONE_URL}/types", data=TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW, headers=HEADERS)

        assert res.status_code == HTTPStatus.OK
        assert json.dumps(TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW) == authorization_mock.call_args[1]["data"]

    async def test_route_request__pass_method_to_authorization_service(
        self,
        authorization_mock,
        app,
        client,
        mocked_document_type_request,
        document_type_source_cache,
        authorization_middleware,
    ):
        document_type_source_cache.clear()

        authorization_mock.return_value = Response(status_code=200, headers=HEADERS)

        res = await client.get(f"{CORLEONE_URL}/types/111", headers=HEADERS)

        assert res.status_code == HTTPStatus.OK
        assert ("x-original-method", "GET") in authorization_mock.call_args[1]["headers"].items()
