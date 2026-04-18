from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    UNIFIER_BASE_API_PREFIX,
    V1_PREFIX,
)
from tests.data.unifier_json_data import (
    UNIFIED_CELLS_DATA_DICT,
    UNIFIED_CELLS_DATA_JSON,
    UNIFIED_DATA_DICT,
    UNIFIED_DATA_JSON,
    UNIFIED_DATA_NOT_FOUND_DICT,
    UNIFIED_DATA_NOT_FOUND_JSON,
)

UNIFIER_BASE_URL = f"{UNIFIER_BASE_API_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.unifier
async def test_get_unified_data__ok(client, document_id):
    unifier_url = f"{UNIFIER_BASE_URL}/unified_data/{document_id}"
    with aioresponses() as mock_response:
        mock_response.get(unifier_url, body=UNIFIED_DATA_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/unified-data")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UNIFIED_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.unifier
async def test_get_unified_data__not_found(client, document_id):
    unifier_url = f"{UNIFIER_BASE_URL}/unified_data/{document_id}"
    with aioresponses() as mock_response:
        mock_response.get(unifier_url, body=UNIFIED_DATA_NOT_FOUND_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/unified-data")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UNIFIED_DATA_NOT_FOUND_DICT


@pytest.mark.asyncio
@pytest.mark.unifier
async def test_get_unified_cells_data__ok(client, document_id):
    table_id = "table123"
    unifier_url = f"{UNIFIER_BASE_URL}/unified_data/{document_id}/tables/{table_id}/cells"
    with aioresponses() as mock_response:
        mock_response.get(unifier_url, body=UNIFIED_CELLS_DATA_JSON)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/unified-data/tables/{table_id}/cells"
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UNIFIED_CELLS_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.unifier
async def test_get_file_unified_data__ok(client, file_id):
    unifier_url = f"{UNIFIER_BASE_URL}/unified_data/{file_id}"
    with aioresponses() as mock_response:
        mock_response.get(unifier_url, body=UNIFIED_DATA_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/files/{file_id}/unified-data")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UNIFIED_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.unifier
async def test_get_file_unified_data__not_found(client, file_id):
    unifier_url = f"{UNIFIER_BASE_URL}/unified_data/{file_id}"
    with aioresponses() as mock_response:
        mock_response.get(unifier_url, body=UNIFIED_DATA_NOT_FOUND_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/files/{file_id}/unified-data")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UNIFIED_DATA_NOT_FOUND_DICT


@pytest.mark.asyncio
@pytest.mark.unifier
async def test_get_file_unified_cells_data__ok(client, file_id):
    table_id = "table123"
    unifier_url = f"{UNIFIER_BASE_URL}/unified_data/{file_id}/tables/{table_id}/cells"
    with aioresponses() as mock_response:
        mock_response.get(unifier_url, body=UNIFIED_CELLS_DATA_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/files/{file_id}/unified-data/tables/{table_id}/cells")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UNIFIED_CELLS_DATA_DICT
