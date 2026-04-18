from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from aioresponses import aioresponses

from deps_api_gateway.api.endpoints.v1.routers.prototype.helper import (
    PrototypeRouterHelper,
)
from deps_api_gateway.constants import (
    API_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    PROTOTYPE_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from tests.data.extraction_json_data import *
from tests.data.layout_json_data import *
from tests.data.prototype_json_data import *

PROTOTYPE_BASE_URL = f"{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes"
EXTRACTION_V2_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}"
EXTRACTION_V1_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}"
HEADERS = {"deps-token": '{"organisation": "deps-users"}'}


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_get_layouts__valid_response(client, prototype_id):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts"
    with aioresponses() as mock_response:
        mock_response.get(prototype_url, body=LAYOUTS_RESPONSE_JSON)

        response = await client.get(f"{API_PREFIX}/prototypes/{prototype_id}/layouts")

        assert response.status_code == 200
        assert response.json() == LAYOUTS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_get_layouts__no_layouts__valid_response(client, prototype_id):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts"
    with aioresponses() as mock_response:
        mock_response.get(prototype_url, body=NO_LAYOUTS_RESPONSE_JSON)

        response = await client.get(f"{API_PREFIX}/prototypes/{prototype_id}/layouts")

        assert response.status_code == 200
        assert response.json() == NO_LAYOUTS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_delete_layout__no_content(client, prototype_id, layout_id):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts/{layout_id}"
    with aioresponses() as mock_response:
        mock_response.delete(prototype_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(f"{API_PREFIX}/prototypes/{prototype_id}/layouts/{layout_id}")

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_delete_layout__bad_request(client, prototype_id, layout_id):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts/{layout_id}"
    with aioresponses() as mock_response:
        mock_response.delete(prototype_url, status=HTTPStatus.BAD_REQUEST)

        response = await client.delete(f"{API_PREFIX}/prototypes/{prototype_id}/layouts/{layout_id}")

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_delete_layouts__no_content(client, prototype_id, layout_id):
    query_string = {"layoutIds": ["a", "b"]}
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts?{urlencode(query_string, doseq=True)}"
    with aioresponses() as mock_response:
        mock_response.delete(prototype_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(f"{API_PREFIX}/prototypes/{prototype_id}/layouts", params=query_string)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_delete_layouts__bad_request(client, prototype_id, layout_id):
    query_string = {"layoutIds": ["a", "b"]}
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts?{urlencode(query_string, doseq=True)}"
    with aioresponses() as mock_response:
        mock_response.delete(prototype_url, status=HTTPStatus.BAD_REQUEST)

        response = await client.delete(f"{API_PREFIX}/prototypes/{prototype_id}/layouts", params=query_string)

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_get_layout__valid_response(client, prototype_id, layout_id):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts/{layout_id}"
    with aioresponses() as mock_response:
        mock_response.get(
            prototype_url,
            body=LAYOUT_WITH_UNIFIED_DATA_AND_DOCUMENT_LAYOUT_RESPONSE_JSON,
            status=HTTPStatus.OK,
        )
        response = await client.get(f"{API_PREFIX}/prototypes/{prototype_id}/layouts/{layout_id}", headers=HEADERS)

        assert response.status_code == 200
        assert response.json() == LAYOUT_WITH_UNIFIED_DATA_AND_DOCUMENT_LAYOUT_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_get_layout__not_found_layout__bad_request(client, prototype_id, layout_id):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts/{layout_id}"
    with aioresponses() as mock_response:
        mock_response.get(
            prototype_url,
            status=HTTPStatus.BAD_REQUEST,
            body=LAYOUT_NOT_FOUND_RESPONSE_DICT,
        )
        response = await client.get(f"{API_PREFIX}/prototypes/{prototype_id}/layouts/{layout_id}", headers=HEADERS)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert json.loads(response.content) == LAYOUT_NOT_FOUND_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_get_layout__not_found_prototype__bad_request(client, prototype_id, layout_id):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/layouts/{layout_id}"
    with aioresponses() as mock_response:
        mock_response.get(
            prototype_url,
            status=HTTPStatus.BAD_REQUEST,
            body=LAYOUT_NOT_FOUND_RESPONSE_DICT,
        )
        response = await client.get(f"{API_PREFIX}/prototypes/{prototype_id}/layouts/{layout_id}", headers=HEADERS)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert json.loads(response.content) == LAYOUT_NOT_FOUND_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_route_field_creation(client, prototype_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}/mappings"
    extraction_url = f"{EXTRACTION_V2_BASE_URL}/document-types/{prototype_id}/extraction-fields"

    with aioresponses() as mock_response:
        mock_response.post(
            prototype_url,
            status=HTTPStatus.CREATED,
            body=PROTOTYPE_MAPPING_RESPONSE__JSON,
        )
        mock_response.post(
            extraction_url,
            status=HTTPStatus.CREATED,
            body=EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
        )

        response = await client.post(
            f"{PROTOTYPE_BASE_URL}/{prototype_id}/fields",
            json=PROTOTYPE_EF_CREATE_REQUEST_DICT,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert json.loads(response.content) == EXPECTED_CONSOLIDATED__FIELD_WITH_MAPPING_DICT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_route_field_updation(client, prototype_id: str):
    field_code = "test_code"
    extraction_url = f"{EXTRACTION_V2_BASE_URL}/document-types/{prototype_id}/extraction-fields/{field_code}"

    with aioresponses() as mock_response:
        mock_response.patch(
            extraction_url,
            status=HTTPStatus.OK,
            body=EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
        )

        response = await client.patch(
            f"{PROTOTYPE_BASE_URL}/{prototype_id}/fields/{field_code}",
            json=PROTOTYPE_EF_UPDATE_REQUEST_DICT,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_route_field_deletion(client, prototype_id: str):
    field_code = "test_code"
    extraction_url = f"{EXTRACTION_V2_BASE_URL}/document-types/{prototype_id}/extraction-fields?fieldCodes={field_code}"

    with aioresponses() as mock_response:
        mock_response.delete(
            extraction_url,
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(
            f"{PROTOTYPE_BASE_URL}/{prototype_id}/fields/{field_code}",
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.prototype
async def test_route_searching_for_prototypes(client, prototype_id: str):
    prototype_url = f"{PROTOTYPE_BASE_URL}/{prototype_id}"
    extraction_url = f"{EXTRACTION_V1_BASE_URL}/document-types/{prototype_id}"

    with aioresponses() as mock_response:
        mock_response.get(
            prototype_url,
            status=HTTPStatus.OK,
            body=PROTOTYPE_DOCUMENT_TYPE_RESPONSE__JSON,
        )

        mock_response.get(
            extraction_url,
            status=HTTPStatus.OK,
            body=EXTRACTION_DOCUMENT_TYPE_RESPONSE__JSON,
        )

        response = await client.get(
            f"{PROTOTYPE_BASE_URL}/{prototype_id}",
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == EXPECTED_CONSOLIDATED__PROTOTYPE_WITH_EXTRACTION_RESPONSE_DICT


@pytest.mark.prototype
def test_route_helper__extract_prototype_id_from_url():
    id_ = "64b8a9c4fd8e477b899921a1d95eb964"
    url = f"http://localhost:8000/api/prototype/v1/prototypes/{id_}"

    assert PrototypeRouterHelper.extract_prototype_id_from_url(url) == id_


@pytest.mark.prototype
def test_route_helper__extract_field_code_from_url():
    code = "64b8a9c4fd8"
    url = f"http://localhost:8000/api/prototype/v1/prototypes/64b8a9c4fd8e477b899921a1d95eb964/fields/{code}"

    assert PrototypeRouterHelper.extract_field_code_from_url(url) == code


@pytest.mark.prototype
def test_route_helper__type_updation_for_one2many_mapping():
    data = {
        "typeCode": "test",
        "description": "test",
    }

    expected_data = {
        "description": {
            "baseType": "test",
            "baseTypeMeta": "test",
        },
        "typeCode": "list",
    }

    assert PrototypeRouterHelper.update_field_data_according_for_one2many_mapping(data) == expected_data
