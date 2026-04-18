import copy
import json
import urllib
from http import HTTPStatus

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    FILES_BATCH_BASE_API_PREFIX,
    V1_PREFIX,
)
from tests.data.batch_json_data import (
    ADD_BATCH_FILES_REQUEST,
    BATCH_CREATE_REQUEST,
    GET_BATCH_INFO,
    GET_BATCHES_RESPONSE,
)

API_GATEWAY_BATCH_V5_URL = f"{BASE_API_V5_PREFIX}/batches"
FILES_BATCH_BASE_V1_URL = f"{FILES_BATCH_BASE_API_PREFIX}{V1_PREFIX}/batches"


@pytest.mark.asyncio
@pytest.mark.batches
async def test_get_batches__ok(client: AsyncClient):
    params = {
        "page": 0,
        "perPage": 2,
        "sortBy": "created_at",
        "sortOrder": "desc",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BATCH_BASE_V1_URL}?{urllib.parse.urlencode(params, doseq=True)}",
            status=HTTPStatus.OK,
            payload=GET_BATCHES_RESPONSE,
        )

        response = await client.get(API_GATEWAY_BATCH_V5_URL, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_BATCHES_RESPONSE


@pytest.mark.asyncio
@pytest.mark.batches
async def test_create_batch__ok(client: AsyncClient):
    batch = {
        "id": "1",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            FILES_BATCH_BASE_V1_URL,
            status=HTTPStatus.CREATED,
            body=json.dumps(batch),
        )

        response = await client.post(API_GATEWAY_BATCH_V5_URL, json=BATCH_CREATE_REQUEST)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == batch


@pytest.mark.asyncio
@pytest.mark.batches
async def test_create_batch__group_not_found(client, faker):
    missing_group_id = faker.uuid4()

    data = copy.deepcopy(BATCH_CREATE_REQUEST)
    data["groupId"] = missing_group_id

    with aioresponses() as mock:
        mock.post(
            FILES_BATCH_BASE_V1_URL,
            status=HTTPStatus.NOT_FOUND,
        )

        response = await client.post(API_GATEWAY_BATCH_V5_URL, json=data)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.batches
async def test_get_batch_info__ok(client, faker):
    batch_id = faker.uuid4()

    with aioresponses() as mock:
        mock.get(f"{FILES_BATCH_BASE_V1_URL}/{batch_id}", status=HTTPStatus.OK, body=json.dumps(GET_BATCH_INFO))

        response = await client.get(f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_BATCH_INFO


@pytest.mark.asyncio
@pytest.mark.batches
async def test_get_batch_info__not_found(client, faker):
    batch_id = faker.uuid4()
    body = {"code": "not_found", "message": "something went wrong"}

    with aioresponses() as mock:
        mock.get(f"{FILES_BATCH_BASE_V1_URL}/{batch_id}", status=HTTPStatus.NOT_FOUND, body=json.dumps(body))

        response = await client.get(f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_batch__ok(client, faker):
    document_id = faker.uuid4()

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}?ids={document_id}&ids={document_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(f"{API_GATEWAY_BATCH_V5_URL}?ids={document_id}&ids={document_id}")

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_batch__error(client, faker):
    document_id = faker.uuid4()
    body = {"code": "bad_request", "message": "something went wrong"}

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}?ids={document_id}&ids={document_id}",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(body),
        )

        response = await client.delete(f"{API_GATEWAY_BATCH_V5_URL}?ids={document_id}&ids={document_id}")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_batch_with_documents__ok(client, faker):
    document_id = faker.uuid4()

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}/with-documents?ids={document_id}&ids={document_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(f"{API_GATEWAY_BATCH_V5_URL}/with-documents?ids={document_id}&ids={document_id}")

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_batch_with_documents__error(client, faker):
    document_id = faker.uuid4()
    body = {"code": "bad_request", "message": "something went wrong"}

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}/with-documents?ids={document_id}&ids={document_id}",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(body),
        )

        response = await client.delete(f"{API_GATEWAY_BATCH_V5_URL}/with-documents?ids={document_id}&ids={document_id}")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_files__ok(client, faker):
    batch_id = faker.uuid4()
    document_id = faker.uuid4()

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}/{batch_id}/files?ids={document_id}&ids={document_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(
            f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}/files?ids={document_id}&ids={document_id}",
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_files__error(client, faker):
    batch_id = faker.uuid4()
    document_id = faker.uuid4()
    body = {"code": "bad_request", "message": "something went wrong"}

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}/{batch_id}/files?ids={document_id}&ids={document_id}",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(body),
        )

        response = await client.delete(
            f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}/files?ids={document_id}&ids={document_id}",
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_files_with_documents__ok(client, faker):
    batch_id = faker.uuid4()
    document_id = faker.uuid4()

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}/{batch_id}/files/with-documents?ids={document_id}&ids={document_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(
            f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}/files/with-documents?ids={document_id}&ids={document_id}",
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.batches
async def test_delete_files_with_documents__error(client, faker):
    batch_id = faker.uuid4()
    document_id = faker.uuid4()
    body = {"code": "bad_request", "message": "something went wrong"}

    with aioresponses() as mock:
        mock.delete(
            f"{FILES_BATCH_BASE_V1_URL}/{batch_id}/files/with-documents?ids={document_id}&ids={document_id}",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(body),
        )

        response = await client.delete(
            f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}/files/with-documents?ids={document_id}&ids={document_id}",
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.batches
async def test_add_files__ok(client: AsyncClient, faker):
    batch_id = faker.uuid4()

    with aioresponses() as mock_response:
        mock_response.post(f"{FILES_BATCH_BASE_V1_URL}/{batch_id}/files", status=HTTPStatus.CREATED)

        response = await client.post(f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}/files", json=ADD_BATCH_FILES_REQUEST)

        assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
@pytest.mark.batches
async def test_add_files__error(client: AsyncClient, faker):
    batch_id = faker.uuid4()
    body = {"code": "not_found_error", "message": "batch not found"}

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BATCH_BASE_V1_URL}/{batch_id}/files", status=HTTPStatus.NOT_FOUND, body=json.dumps(body)
        )

        response = await client.post(f"{API_GATEWAY_BATCH_V5_URL}/{batch_id}/files", json=ADD_BATCH_FILES_REQUEST)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body
