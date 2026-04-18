import json
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_V1_PREFIX,
    BASE_API_V5_PREFIX,
    ENRICHMENT_BASE_PREFIX,
    V1_PREFIX,
)
from tests.data.enrichment_json_data import (
    CREATE_EXTRA_FIELD_RESPONSE_DICT,
    CREATE_EXTRA_FIELD_RESPONSE_JSON,
    CREATE_OR_MODIFY_SUPPLEMENT_ENTITY_DICT,
    CREATE_OR_MODIFY_SUPPLEMENT_ENTITY_JSON,
    SUPPLEMENT_DATA_CREATE_OR_PUT_DICT,
    SUPPLEMENT_DATA_DICT,
    SUPPLEMENT_DATA_JSON,
    SUPPLEMENT_NOT_FOUND_RESPONSE_DICT,
    SUPPLEMENT_NOT_FOUND_RESPONSE_JSON,
)

ENRICHMENT_BASE_URL = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}/document-types"


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_create_extra_field__ok(client: AsyncClient, document_type_id):
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    with aioresponses() as mock_response:
        mock_response.post(enrichment_url, body=CREATE_EXTRA_FIELD_RESPONSE_JSON, status=HTTPStatus.CREATED)

        response = await client.post(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            data=json.dumps({"name": "ef_name", "order": 0}),
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CREATE_EXTRA_FIELD_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_create_extra_field__bad_request(client: AsyncClient, document_type_id):
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    with aioresponses() as mock_response:
        mock_response.post(enrichment_url, status=HTTPStatus.BAD_REQUEST)

        response = await client.post(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            data=json.dumps({"name": "ef_name", "order": 0}),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_delete_extra_fields__ok(client: AsyncClient, document_type_id):
    params = {"extraFieldCodes": "ef_code"}
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields?{urlencode(params, doseq=True)}"
    with aioresponses() as mock_response:
        mock_response.delete(enrichment_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            params=params,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_delete_extra_fields__bad_request(client: AsyncClient, document_type_id):
    params = {"extraFieldCodes": "ef_code"}
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields?{urlencode(params, doseq=True)}"
    with aioresponses() as mock_response:
        mock_response.delete(enrichment_url, status=HTTPStatus.BAD_REQUEST)

        response = await client.delete(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            params=params,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_delete_extra_fields__forbidden(client: AsyncClient, document_type_id):
    params = {"extraFieldCodes": "ef_code"}
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields?{urlencode(params, doseq=True)}"
    with aioresponses() as mock_response:
        mock_response.delete(enrichment_url, status=HTTPStatus.FORBIDDEN)

        response = await client.delete(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            params=params,
        )

        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_get_extra_fields__ok(client: AsyncClient, document_type_id):
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    fields = {"fields": {"name": "ef_name"}}
    with aioresponses() as mock_response:
        mock_response.get(enrichment_url, status=HTTPStatus.OK, body=json.dumps(fields))

        response = await client.get(f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == fields


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_get_extra_fields__bad_request(client: AsyncClient, document_type_id):
    details = {"details": "Not found"}
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    with aioresponses() as mock_response:
        mock_response.get(enrichment_url, status=HTTPStatus.NOT_FOUND, body=json.dumps(details))

        response = await client.get(f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields")

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_get_extra_fields__not_found(client: AsyncClient, document_type_id):
    exception = {"code": "document_type_not_found", "message": "Not found"}
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    with aioresponses() as mock_response:
        mock_response.get(enrichment_url, status=HTTPStatus.NOT_FOUND, body=json.dumps(exception))

        response = await client.get(f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == exception


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_create_or_modify_supplement__ok(client: AsyncClient, document_id):
    enrichment_url = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}/supplements/{document_id}"
    with aioresponses() as mock_response:
        mock_response.put(enrichment_url, body=CREATE_OR_MODIFY_SUPPLEMENT_ENTITY_JSON, status=HTTPStatus.OK)

        response = await client.put(
            f"{BASE_API_V1_PREFIX}/documents/{document_id}/supplements",
            data=json.dumps(SUPPLEMENT_DATA_CREATE_OR_PUT_DICT),
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == CREATE_OR_MODIFY_SUPPLEMENT_ENTITY_DICT


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_find_supplement__ok(client: AsyncClient, document_id):
    enrichment_url = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}/supplements/{document_id}"
    with aioresponses() as mock_response:
        mock_response.get(enrichment_url, body=SUPPLEMENT_DATA_JSON, status=HTTPStatus.OK)

        response = await client.get(f"{BASE_API_V1_PREFIX}/documents/{document_id}/supplements")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == SUPPLEMENT_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_find_supplement__not_found(client: AsyncClient, document_id):
    enrichment_url = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}/supplements/{document_id}"
    with aioresponses() as mock_response:
        mock_response.get(enrichment_url, body=SUPPLEMENT_NOT_FOUND_RESPONSE_JSON, status=HTTPStatus.NOT_FOUND)

        response = await client.get(f"{BASE_API_V1_PREFIX}/documents/{document_id}/supplements")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert json.loads(response.content)["code"] == SUPPLEMENT_NOT_FOUND_RESPONSE_DICT["code"]
        assert json.loads(response.content)["message"] == SUPPLEMENT_NOT_FOUND_RESPONSE_DICT["message"]


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_update_extra_fields__ok(client: AsyncClient, document_type_id):
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    with aioresponses() as mock_response:
        mock_response.put(enrichment_url, status=HTTPStatus.OK)

        response = await client.put(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            data=json.dumps({"extraFields": [{"name": "ef name", "code": "ef_code", "order": 1}]}),
        )

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_update_extra_fields__not_found(client: AsyncClient, document_type_id):
    exception = {"code": "document_type_not_found", "message": "Not found"}
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    with aioresponses() as mock_response:
        mock_response.put(enrichment_url, status=HTTPStatus.NOT_FOUND, body=json.dumps(exception))

        response = await client.put(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            data=json.dumps({"extraFields": [{"name": "ef name", "code": "ef_code", "order": 1}]}),
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == exception


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_update_extra_fields__forbidden(client: AsyncClient, document_type_id):
    exception = {"code": "forbidden_error", "message": "Forbidden"}
    enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
    with aioresponses() as mock_response:
        mock_response.put(enrichment_url, status=HTTPStatus.FORBIDDEN, body=json.dumps(exception))

        response = await client.put(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
            data=json.dumps({"extraFields": [{"name": "ef name", "code": "ef_code", "order": 1}]}),
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == exception


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_update_extra_fields__service_unavailable(client: AsyncClient, document_type_id):
    response = await client.put(
        f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extra-fields",
        data=json.dumps({"extraFields": [{"name": "ef name", "code": "ef_code", "order": 1}]}),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["code"] == "enrichment_error"


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_get_document_supplement(client: AsyncClient, document_id: str):
    url = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}/supplements/{document_id}"

    with aioresponses() as mock_response:
        mock_response.get(url, status=HTTPStatus.OK, body=SUPPLEMENT_DATA_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/supplement")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == SUPPLEMENT_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.enrichment
async def test_save_document_supplement__ok(client: AsyncClient, document_id: str):
    url = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}/supplements/{document_id}"
    data = {"data": [{"name": "string", "value": "string", "code": "string"}], "documentTypeId": "string"}
    expecter_response = {"entityId": "string"}

    with aioresponses() as mock_response:
        mock_response.put(url, status=HTTPStatus.OK, body=json.dumps(expecter_response))

        response = await client.put(f"{BASE_API_V5_PREFIX}/documents/{document_id}/supplement", data=json.dumps(data))

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expecter_response
