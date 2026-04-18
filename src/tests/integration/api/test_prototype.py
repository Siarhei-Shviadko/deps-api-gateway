import copy
from datetime import datetime
from http import HTTPStatus
from typing import Optional
from unittest.mock import mock_open, patch

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.application import GetPrototypeExtras, HeaderType
from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    PARSING_BASE_API_PREFIX,
    PROTOTYPE_BASE_API_PREFIX,
    UNIFIER_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from tests.data.extraction_json_data import *
from tests.data.layout_json_data import *
from tests.data.parsing_json_data import *
from tests.data.prototype_json_data import *
from tests.data.unifier_json_data import *

PROTOTYPE_BASE_URL = f"{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes"
EXTRACTION_V2_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}"
EXTRACTION_V1_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}"
UNIFIER_BASE_URL = f"{UNIFIER_BASE_API_PREFIX}{V1_PREFIX}"
PARSING_BASE_URL = f"{PARSING_BASE_API_PREFIX}{V1_PREFIX}"
HEADERS = {"deps-token": '{"organisation": "deps-users"}'}


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_mapping_creation(client: AsyncClient, prototype_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/mappings"

    with aioresponses() as mock_response:
        mock_response.post(
            prototype_url,
            status=HTTPStatus.CREATED,
            body=PROTOTYPE_MAPPING_RESPONSE__JSON,
        )

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/document-types/{prototype_id}/prototype/mappings",
            json=PROTOTYPE_MAPPING_CREATE_REQUEST_DICT,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert json.loads(response.content) == PROTOTYPE_MAPPING_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_mapping_updation(client: AsyncClient, prototype_id: str):
    field_code = "test_code"
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/mappings/{field_code}"

    with aioresponses() as mock_response:
        mock_response.put(
            prototype_url,
            status=HTTPStatus.OK,
            body=PROTOTYPE_MAPPING_RESPONSE__JSON,
        )

        response = await client.put(
            f"{BASE_API_V5_PREFIX}/document-types/{prototype_id}/prototype/mappings/{field_code}",
            json=PROTOTYPE_MAPPING_UPDATE_REQUEST_DICT,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == PROTOTYPE_MAPPING_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_tabular_mapping_creation(client: AsyncClient, prototype_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/tabular-mappings"

    with aioresponses() as mock_response:
        mock_response.post(
            prototype_url,
            status=HTTPStatus.CREATED,
            body=PROTOTYPE_TABULAR_MAPPING_RESPONSE__JSON,
        )

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/document-types/{prototype_id}/prototype/tabular-mappings",
            json=PROTOTYPE_TABULAR_MAPPING_REQUEST_DICT,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert json.loads(response.content) == PROTOTYPE_TABULAR_MAPPING_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_update_tabular_mapping(client: AsyncClient, prototype_id: str, field_code: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/tabular-mappings/{field_code}"

    data = {
        "headerType": HeaderType.ROWS.value,
        "headers": [{"name": "name", "aliases": ["name1", "name2"]}],
        "occurrenceIndex": -1,
    }

    with aioresponses() as mock_response:
        mock_response.patch(
            prototype_url,
            status=HTTPStatus.OK,
            body=PROTOTYPE_TABULAR_MAPPING_RESPONSE__JSON,
        )

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/document-types/{prototype_id}/prototype/tabular-mappings/{field_code}",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == PROTOTYPE_TABULAR_MAPPING_RESPONSE_DICT


@pytest.mark.parametrize(
    "extras",
    (
        [GetPrototypeExtras.LAYOUTS.value],
        None,
    ),
)
@pytest.mark.asyncio
@pytest.mark.prototype
async def test_searching_for_prototypes__ok(
    client: AsyncClient, prototype_id: str, extras: Optional[list[GetPrototypeExtras]]
):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}"
    prototype_layouts_url = f"{prototype_url}/layouts"
    extraction_url = f"{EXTRACTION_V1_BASE_URL}/document-types/{prototype_id}"

    data = {}
    if extras is not None:
        data["extras"] = extras

    expected_response = copy.deepcopy(EXPECTED_CONSOLIDATED__PROTOTYPE_WITH_EXTRACTION_RESPONSE_DICT)
    expected_response["referenceLayouts"] = None

    with aioresponses() as mock_response:
        mock_response.get(prototype_url, status=HTTPStatus.OK, body=PROTOTYPE_DOCUMENT_TYPE_RESPONSE__JSON)
        mock_response.get(prototype_layouts_url, status=HTTPStatus.OK, body=GET_REFERENCE_LAYOUTS_RESPONSE_JSON)
        mock_response.get(extraction_url, status=HTTPStatus.OK, body=EXTRACTION_DOCUMENT_TYPE_RESPONSE__JSON)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/document-types/{prototype_id}/prototype",
            headers=HEADERS,
            params=data,
        )

        assert response.status_code == HTTPStatus.OK

        if extras is not None and GetPrototypeExtras.LAYOUTS in extras:
            expected_response["referenceLayouts"] = GET_REFERENCE_LAYOUTS_RESPONSE_DICT["reference_layouts"]

        assert response.json() == expected_response


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_create_prototype__created(client: AsyncClient):
    prototype_url = f"{PROTOTYPE_BASE_URL}"
    data = {
        "name": "string",
        "engine": "TESSERACT",
        "language": "en",
        "description": "string",
    }
    expected_response = {"id": "string"}

    with aioresponses() as mock_response:
        mock_response.post(prototype_url, status=HTTPStatus.CREATED, body=json.dumps(expected_response))

        response = await client.post(f"{BASE_API_V5_PREFIX}/document-types/prototype", json=data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == expected_response


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_get_reference_layouts__ok(client: AsyncClient, document_type_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{document_type_id}/layouts"

    with aioresponses() as mock_response:
        mock_response.get(prototype_url, status=HTTPStatus.OK, body=GET_REFERENCE_LAYOUTS_RESPONSE_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/prototype/layouts")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_REFERENCE_LAYOUTS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_get_reference_layout__ok(client: AsyncClient, document_type_id: str, layout_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{document_type_id}/layouts/{layout_id}"
    unified_data_url = f"{UNIFIER_BASE_URL}/unified_data/{layout_id}"
    parsing_url = f"{PARSING_BASE_URL}/document-layout/{layout_id}/info"

    with aioresponses() as mock_response:
        mock_response.get(prototype_url, status=HTTPStatus.OK, body=GET_REFERENCE_LAYOUT_RESPONSE_JSON)
        mock_response.get(unified_data_url, status=HTTPStatus.OK, body=UNIFIED_DATA_JSON)
        mock_response.get(parsing_url, status=HTTPStatus.OK, body=PARSING_INFO_JSON)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/prototype/layouts/{layout_id}"
        )

        assert response.status_code == HTTPStatus.OK
        json_result = response.json()
        assert json_result["unifiedData"] == UNIFIED_DATA_DICT
        assert json_result["documentLayoutData"] == PARSING_INFO_DICT
        assert all(key in json_result for key in GET_REFERENCE_LAYOUT_RESPONSE_DICT.keys())


@pytest.mark.asyncio
async def test_get_reference_layout__no_unified_data__ok(client: AsyncClient, document_type_id: str, layout_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{document_type_id}/layouts/{layout_id}"
    unified_data_url = f"{UNIFIER_BASE_URL}/unified_data/{layout_id}"
    parsing_url = f"{PARSING_BASE_URL}/document-layout/{layout_id}/info"

    with aioresponses() as mock_response:
        mock_response.get(prototype_url, status=HTTPStatus.OK, body=GET_REFERENCE_LAYOUT_RESPONSE_JSON)
        mock_response.get(unified_data_url, status=HTTPStatus.NOT_FOUND)
        mock_response.get(parsing_url, status=HTTPStatus.NOT_FOUND)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/prototype/layouts/{layout_id}"
        )

        assert response.status_code == HTTPStatus.OK
        json_result = response.json()
        assert json_result["unifiedData"] is None
        assert json_result["documentLayoutData"] is None
        assert all(key in json_result for key in GET_REFERENCE_LAYOUT_RESPONSE_DICT.keys())


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_create_reference_layouts__created(client: AsyncClient, document_type_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{document_type_id}/layouts"
    expected_response = {"id": "string"}

    with patch("builtins.open", mock_open(read_data="file")) as mock_file:
        file = open(mock_file, "rb")
    data = {
        "file": (uuid.uuid4().hex, file),
    }

    with aioresponses() as mock_response:
        mock_response.post(prototype_url, status=HTTPStatus.CREATED, body=json.dumps(expected_response))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/prototype/layouts", files=data
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == expected_response


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_delete_reference_layouts__no_content(client: AsyncClient, document_type_id: str):
    query_string = "layoutIds=1&layoutIds=2"
    prototype_url = f"{PROTOTYPE_BASE_URL}/{document_type_id}/layouts?{query_string}"

    with aioresponses() as mock_response:
        mock_response.delete(prototype_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/prototype/layouts?{query_string}"
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_restart_reference_layout__ok(client: AsyncClient, document_type_id: str, layout_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{document_type_id}/layouts/{layout_id}/restart"

    with aioresponses() as mock_response:
        mock_response.post(prototype_url, status=HTTPStatus.OK)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/prototype/layouts/{layout_id}/pipelines/restart"
        )

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_update_prototype__created(client: AsyncClient):
    document_type_id = uuid.uuid4().hex
    prototype_url = f"{PROTOTYPE_BASE_URL}/{document_type_id}"
    data = {
        "engine": "TESSERACT",
        "language": "en",
        "description": "string",
    }

    expected_response = {
        "id": document_type_id,
        "name": uuid.uuid4().hex,
        "engine": "TESSERACT",
        "language": "en",
        "createdAt": datetime.now().isoformat(),
        "description": "string",
    }

    with aioresponses() as mock_response:
        mock_response.patch(prototype_url, status=HTTPStatus.OK, body=json.dumps(expected_response))

        response = await client.patch(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/prototype", json=data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_response
