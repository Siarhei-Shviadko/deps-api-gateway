import json
import urllib
from http import HTTPStatus

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    SPLITTING_BASE_API_PREFIX,
    V1_PREFIX,
)
from tests.data.splitter_json_data import (
    CREATE_SPLITTER_REQUEST,
    CREATE_SPLITTER_RESPONSE,
    FIND_SPLITTER_RESPONSE,
    FIND_SPLITTERS_RESPONSE,
    UPDATE_SPLITTER_REQUEST,
    UPDATE_SPLITTER_RESPONSE,
)

GATEWAY_SPLITTERS_URL = f"{BASE_API_V5_PREFIX}/splitting/splitters"
SPLITTING_SERVICE_BASE_URL = f"{SPLITTING_BASE_API_PREFIX}{V1_PREFIX}/splitters"


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_find_splitters__ok(client: AsyncClient, faker):
    group_id = faker.uuid4()
    params = {"groupId": group_id}

    with aioresponses() as mock:
        mock.get(
            f"{SPLITTING_SERVICE_BASE_URL}?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.OK,
            payload=FIND_SPLITTERS_RESPONSE,
        )

        response = await client.get(GATEWAY_SPLITTERS_URL, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIND_SPLITTERS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_find_splitter_for__ok(client: AsyncClient, faker):
    group_id = faker.uuid4()
    document_type_id = faker.uuid4()
    params = {"groupId": group_id, "documentTypeId": document_type_id}

    with aioresponses() as mock:
        mock.get(
            f"{SPLITTING_SERVICE_BASE_URL}/resolve?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.OK,
            payload=FIND_SPLITTER_RESPONSE,
        )

        response = await client.get(f"{GATEWAY_SPLITTERS_URL}/resolve", params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIND_SPLITTER_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_find_splitter__ok(client: AsyncClient, faker):
    splitter_id = faker.uuid4()

    with aioresponses() as mock:
        mock.get(
            f"{SPLITTING_SERVICE_BASE_URL}/{splitter_id}",
            status=HTTPStatus.OK,
            body=json.dumps(FIND_SPLITTER_RESPONSE),
        )

        response = await client.get(f"{GATEWAY_SPLITTERS_URL}/{splitter_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIND_SPLITTER_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_find_splitter__not_found(client: AsyncClient, faker):
    splitter_id = faker.uuid4()
    body = {"code": "file_splitter_not_found", "message": "Splitter not found"}

    with aioresponses() as mock:
        mock.get(
            f"{SPLITTING_SERVICE_BASE_URL}/{splitter_id}",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(body),
        )

        response = await client.get(f"{GATEWAY_SPLITTERS_URL}/{splitter_id}")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_create_splitter__ok(client: AsyncClient):
    with aioresponses() as mock:
        mock.post(
            SPLITTING_SERVICE_BASE_URL,
            status=HTTPStatus.CREATED,
            body=json.dumps(CREATE_SPLITTER_RESPONSE),
        )

        response = await client.post(GATEWAY_SPLITTERS_URL, json=CREATE_SPLITTER_REQUEST)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CREATE_SPLITTER_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_create_splitter__without_description__ok(client: AsyncClient):
    with aioresponses() as mock:
        mock.post(
            SPLITTING_SERVICE_BASE_URL,
            status=HTTPStatus.CREATED,
            body=json.dumps(CREATE_SPLITTER_RESPONSE),
        )

        response = await client.post(
            GATEWAY_SPLITTERS_URL,
            json={
                "groupId": "group-id-1",
                "documentTypeId": "doc-type-id-1",
                "name": "New Splitter",
                "query": "Split by sections",
                "llmType": "gpt-4",
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CREATE_SPLITTER_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_create_splitter__with_mode__ok(client: AsyncClient):
    with aioresponses() as mock:
        mock.post(
            SPLITTING_SERVICE_BASE_URL,
            status=HTTPStatus.CREATED,
            body=json.dumps(CREATE_SPLITTER_RESPONSE),
        )

        response = await client.post(
            GATEWAY_SPLITTERS_URL,
            json={**CREATE_SPLITTER_REQUEST, "mode": "SECTION_BASED"},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CREATE_SPLITTER_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_create_splitter__conflict(client: AsyncClient):
    body = {"code": "splitter_already_exists", "message": "Splitter already exists"}

    with aioresponses() as mock:
        mock.post(
            SPLITTING_SERVICE_BASE_URL,
            status=HTTPStatus.CONFLICT,
            body=json.dumps(body),
        )

        response = await client.post(GATEWAY_SPLITTERS_URL, json=CREATE_SPLITTER_REQUEST)

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_update_splitter__ok(client: AsyncClient, faker):
    splitter_id = faker.uuid4()

    with aioresponses() as mock:
        mock.patch(
            f"{SPLITTING_SERVICE_BASE_URL}/{splitter_id}",
            status=HTTPStatus.OK,
            body=json.dumps(UPDATE_SPLITTER_RESPONSE),
        )

        response = await client.patch(f"{GATEWAY_SPLITTERS_URL}/{splitter_id}", json=UPDATE_SPLITTER_REQUEST)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UPDATE_SPLITTER_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_update_splitter__not_found(client: AsyncClient, faker):
    splitter_id = faker.uuid4()
    body = {"code": "file_splitter_not_found", "message": "Splitter not found"}

    with aioresponses() as mock:
        mock.patch(
            f"{SPLITTING_SERVICE_BASE_URL}/{splitter_id}",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(body),
        )

        response = await client.patch(f"{GATEWAY_SPLITTERS_URL}/{splitter_id}", json=UPDATE_SPLITTER_REQUEST)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_remove_splitter__ok(client: AsyncClient, faker):
    splitter_id = faker.uuid4()

    with aioresponses() as mock:
        mock.delete(
            f"{SPLITTING_SERVICE_BASE_URL}/{splitter_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(f"{GATEWAY_SPLITTERS_URL}/{splitter_id}")

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.splitters
async def test_remove_splitter__not_found(client: AsyncClient, faker):
    splitter_id = faker.uuid4()
    body = {"code": "file_splitter_not_found", "message": "Splitter not found"}

    with aioresponses() as mock:
        mock.delete(
            f"{SPLITTING_SERVICE_BASE_URL}/{splitter_id}",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(body),
        )

        response = await client.delete(f"{GATEWAY_SPLITTERS_URL}/{splitter_id}")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body
