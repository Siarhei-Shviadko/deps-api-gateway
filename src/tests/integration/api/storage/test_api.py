import json
import urllib
from http import HTTPStatus

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import BASE_API_V5_PREFIX


@pytest.mark.asyncio
@pytest.mark.storage
async def test_download_file__ok(client: AsyncClient, full_storage_url, request_data, file_name, default_storage):
    test_url = f"{BASE_API_V5_PREFIX}/file/{file_name}"
    params = {"storage": default_storage}

    with aioresponses() as mock_response:
        mock_response.get(
            f"{full_storage_url}/{file_name}?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.OK,
            body=request_data.data,
        )

        response = await client.get(test_url, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.content == request_data.data


@pytest.mark.asyncio
@pytest.mark.storage
async def test_download_file__not_found(
    client: AsyncClient, full_storage_url, request_data, file_name, default_storage
):
    test_url = f"{BASE_API_V5_PREFIX}/file/not_found"
    params = {"storage": default_storage}

    with aioresponses() as mock_response:
        mock_response.get(
            f"{full_storage_url}/not_found?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.NOT_FOUND,
        )

        response = await client.get(test_url, params=params)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.storage
async def test_upload_file_with_unique_path__ok(client: AsyncClient, full_storage_url, request_data, file_name):
    test_url = f"{BASE_API_V5_PREFIX}/file"
    expected_response = {"path": file_name}

    with aioresponses() as mock_response:
        mock_response.post(full_storage_url, status=HTTPStatus.OK, body=json.dumps(expected_response))

        response = await client.post(test_url, data=request_data.data, headers=request_data.headers)

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == expected_response


@pytest.mark.asyncio
@pytest.mark.storage
async def test_upload_file_with_unique_path__without_required_fields__ok(
    client: AsyncClient,
    full_storage_url,
    request_data_without_required,
):
    test_url = f"{BASE_API_V5_PREFIX}/file"

    with aioresponses() as mock_response:
        mock_response.post(full_storage_url, status=HTTPStatus.OK)

        response = await client.post(
            test_url,
            data=request_data_without_required.data,
            headers=request_data_without_required.headers,
        )

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.storage
async def test_upload_file_with_unique_path__error(client: AsyncClient, full_storage_url, request_data, file_path):
    test_url = f"{BASE_API_V5_PREFIX}/file"
    expected_response = {"code": "file not found"}

    with aioresponses() as mock_response:
        mock_response.post(full_storage_url, status=HTTPStatus.NOT_FOUND, body=json.dumps(expected_response))

        response = await client.post(test_url, data=request_data.data, headers=request_data.headers)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert json.loads(response.content) == expected_response


@pytest.mark.asyncio
@pytest.mark.storage
async def test_delete_file__ok(client: AsyncClient, full_storage_url, request_data, file_name, default_storage):
    test_url = f"{BASE_API_V5_PREFIX}/file/{file_name}"
    params = {"storage": default_storage}

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{full_storage_url}/{file_name}?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(test_url, params=params)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.storage
async def test_delete_file__error(client: AsyncClient, full_storage_url, request_data, file_name, default_storage):
    test_url = f"{BASE_API_V5_PREFIX}/file/not_found"
    params = {"storage": default_storage}

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{full_storage_url}/not_found?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.NOT_FOUND,
        )

        response = await client.delete(test_url, params=params)

        assert response.status_code == HTTPStatus.NOT_FOUND
