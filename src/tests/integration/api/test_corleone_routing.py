import copy
from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    CORLEONE_BASE_API_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    V1_PREFIX,
    DocumentTypeSource,
)
from tests.data.json_data import (
    CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
    CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
    DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
    DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
    EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
    EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
    EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
    EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
    TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
    TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
    TYPES_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
    TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
)

URL = f"{CORLEONE_BASE_API_PREFIX}/test"

TYPES_URL = f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/types"
EXTRACTED_DATA_URL = f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/extracted-data"
CORLEONE_EXTRACTED_DATA_FIELD_URL = f"{EXTRACTED_DATA_URL}/111/field"
EXTRACTION_EXTRACTED_DATA_FIELD_URL = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}/extracted-data/111/field"

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}
GENERIC_REST_CLIENT_PATH = (
    "deps_api_gateway.infrastructure.proxies.generic_rest_client.old.OldGenericRestClient.request"
)


@pytest.fixture()
def mocked_document_types_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": copy.deepcopy(TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW),
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": copy.deepcopy(TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW),
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.fixture()
def mocked_document_type_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
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
    )
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=async_mock)
    # mocker.patch(GENERIC_REST_CLIENT_NEW, side_effect=async_mock)
    return async_mock


@pytest.fixture()
def mocked_extracted_data_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.fixture()
def mocked_field_chunk_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.mark.asyncio
async def test_routing__get__200(client):
    with aioresponses() as mocked:
        mocked.get(URL, status=200, body=TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW)
        res = await client.get(URL, headers=HEADERS)

        mocked.assert_called_once()
        assert res.status_code == HTTPStatus.OK
        assert res.json() == TYPES_RESPONSE_FROM_CORLEONE_SERVICE_JSON


@pytest.mark.asyncio
async def test_routing__post__201(client):
    with aioresponses() as mocked:
        mocked.post(URL, status=201, body=TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW)
        res = await client.post(URL, headers=HEADERS)

        mocked.assert_called_once()
        assert res.status_code == HTTPStatus.CREATED
        assert res.json() == TYPES_RESPONSE_FROM_CORLEONE_SERVICE_JSON


@pytest.mark.asyncio
async def test_routing__put__403(client):
    with aioresponses() as mocked:
        mocked.put(f"{URL}?rowsPerChunk=15", status=403)
        res = await client.put(f"{URL}?rowsPerChunk=15", headers=HEADERS)

        assert res.status_code == HTTPStatus.FORBIDDEN
        mocked.assert_called_once()


@pytest.mark.asyncio
async def test_routing__delete__204(client):
    with aioresponses() as mocked:
        mocked.delete(f"{URL}/2", status=204)
        res = await client.delete(f"{URL}/2", headers=HEADERS)

        mocked.assert_called_once()
        assert res.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_routing__patch__200(client):
    with aioresponses() as mocked:
        mocked.patch(URL, status=200)
        res = await client.patch(URL, headers=HEADERS)

        mocked.assert_called_once()
        assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_aggregate_document_types__successful(
    client,
    mocked_document_types_request,
    document_type_source_cache,
    document_type_extraction_type_cache,
):
    document_type_source_cache.clear()

    res = await client.get(TYPES_URL, headers=HEADERS)
    doc_types = res.json()["result"]
    doc_type_codes = [el["code"] for el in doc_types]

    assert len(doc_types) == len(TYPES_RESPONSE_FROM_CORLEONE_SERVICE_JSON["result"]) + len(
        TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON
    )
    assert res.status_code == HTTPStatus.OK

    for code in doc_type_codes:
        assert code in document_type_source_cache
        assert code in document_type_extraction_type_cache


@pytest.mark.asyncio
async def test_aggregate_document_types__services_unavailable__error(client):
    res = await client.get(TYPES_URL, headers=HEADERS)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "document_type_response, corleone_response",
    [
        (
            {
                "content": copy.deepcopy(TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW),
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            Exception,
            {
                "content": copy.deepcopy(TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW),
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_aggregate_document_types__one_of_services_unavailable__no_errors(
    client,
    mocked_document_types_request,
    corleone_response,
    document_type_response,
):
    mocked_document_types_request.side_effect = [corleone_response, document_type_response]
    res = await client.get(TYPES_URL, headers=HEADERS)

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_route_document_type__both_services_available__successful(
    client,
    mocked_document_type_request,
    document_type_source_cache,
    document_type_extraction_type_cache,
):
    document_type_source_cache.clear()

    res = await client.get(f"{TYPES_URL}/1", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK

    document_type = res.json()

    assert document_type["code"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"]
    assert document_type["code"] in document_type_source_cache
    assert document_type["code"] in document_type_extraction_type_cache
    assert document_type_extraction_type_cache[document_type["code"]] == document_type["extractionType"]


@pytest.mark.asyncio
async def test_route_document_type__both_services_unavailable__error(client):
    res = await client.get(f"{TYPES_URL}/1", headers=HEADERS)

    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "document_type_response, corleone_response",
    [
        (
            {
                "content": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            Exception,
            {
                "content": TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_route_document_type__one_of_services_unavailable__success(
    client, mocked_document_type_request, corleone_response, document_type_response, document_type_source_cache
):
    document_type_source_cache.clear()

    mocked_document_type_request.side_effect = [corleone_response, document_type_response]
    res = await client.get(f"{TYPES_URL}/1", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_route_document_type__doc_type_in_corleone_service__success(
    client,
    mocked_document_type_request,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    mocked_document_type_request.side_effect = [
        {
            "content": TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    document_type_code = TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON["code"]

    res = await client.get(f"{TYPES_URL}/{document_type_code}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json()["code"] == document_type_code


@pytest.mark.asyncio
async def test_route_document_type__doc_type_in_document_type_service__success(
    client,
    mocked_document_type_request,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    mocked_document_type_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]

    document_type_code = TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"]

    res = await client.get(f"{TYPES_URL}/{document_type_code}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json()["code"] == document_type_code


@pytest.mark.asyncio
async def test_route_document_type__doc_type_from_document_type_service_cached__success(
    client,
    mocked_document_type_request,
    document_type_source_cache,
):
    document_type_code = TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"]
    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE

    mocked_document_type_request.side_effect = [
        {
            "content": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{TYPES_URL}/{document_type_code}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json()["code"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"]


@pytest.mark.asyncio
async def test_route_document_type__doc_type_from_corleone_service_cached__success(
    client,
    mocked_document_type_request,
    document_type_source_cache,
):
    document_type_code = TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON["code"]
    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE

    mocked_document_type_request.side_effect = [
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

    res = await client.get(f"{TYPES_URL}/{document_type_code}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json()["code"] == TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON["code"]


@pytest.mark.asyncio
async def test_route_extracted_data__both_services_available__successful(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    res = await client.get(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_extracted_data__both_services_unavailable__error(client):
    res = await client.get(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "extraction_response, corleone_response",
    [
        (
            {
                "content": EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            Exception,
            {
                "content": EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_route_extracted_data__one_of_services_unavailable__success(
    client, mocked_extracted_data_request, corleone_response, extraction_response, document_type_source_cache
):
    document_type_source_cache.clear()

    mocked_extracted_data_request.side_effect = [corleone_response, extraction_response]
    res = await client.get(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_route_extracted_data__document_type_from_corleone__successful(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_extracted_data__document_type_from_corleone__error(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_route_extracted_data__document_type_from_type__successful(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_extracted_data_request.side_effect = [
        {
            "content": EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_extracted_data__document_type_from_type__error(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.fixture()
def mocked_delete_extracted_data_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.mark.asyncio
async def test_route_delete_extracted_data__both_services_available__successful(
    client,
    mocked_delete_extracted_data_request,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    res = await client.delete(f"{EXTRACTED_DATA_URL}/1/fields", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_delete_extracted_data__both_services_unavailable__error(client, document_type_source_cache):
    document_type_source_cache.clear()

    res = await client.delete(f"{EXTRACTED_DATA_URL}/1/fields", headers=HEADERS)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "corleone_response, extraction_response",
    [
        (
            {
                "content": DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            Exception,
            {
                "content": DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_route_delete_extracted_data__one_of_services_unavailable__success(
    client, mocked_delete_extracted_data_request, corleone_response, extraction_response, document_type_source_cache
):
    document_type_source_cache.clear()

    mocked_extracted_data_request.side_effect = [corleone_response, extraction_response]
    res = await client.delete(f"{EXTRACTED_DATA_URL}/1/fields", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_route_delete_extracted_data__document_type_from_corleone__successful(
    client,
    mocked_delete_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "corleone_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    res = await client.delete(f"{EXTRACTED_DATA_URL}/1/fields", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_delete_extracted_data__document_type_from_corleone__error(
    client,
    mocked_delete_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "corleone_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_delete_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.delete(f"{EXTRACTED_DATA_URL}/1/fields", headers=HEADERS)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_route_delete_extracted_data__document_type_from_type__successful(
    client,
    mocked_delete_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "doc_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_delete_extracted_data_request.side_effect = [
        {
            "content": DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]

    res = await client.delete(f"{EXTRACTED_DATA_URL}/1/fields", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_delete_extracted_data__document_type_from_type__error(
    client,
    mocked_delete_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "doc_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_delete_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.delete(f"{EXTRACTED_DATA_URL}/1/fields", headers=HEADERS)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "explanation,corleone_params,extraction_params,expected_params",
    [
        (
            "Only corleone available",
            dict(status=HTTPStatus.OK, payload=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON),
            dict(
                status=HTTPStatus.BAD_REQUEST,
            ),
            dict(status=HTTPStatus.OK, payload=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON),
        ),
        (
            "Only extraction service available",
            dict(
                status=HTTPStatus.BAD_REQUEST,
            ),
            dict(status=HTTPStatus.OK, payload=EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON),
            dict(status=HTTPStatus.OK, payload=EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON),
        ),
        (
            "Both services available",
            dict(status=HTTPStatus.OK, payload=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON),
            dict(status=HTTPStatus.OK, payload=EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON),
            dict(status=HTTPStatus.OK, payload=EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON),
        ),
        (
            "Both unavailable",
            dict(
                status=HTTPStatus.BAD_REQUEST,
            ),
            dict(status=HTTPStatus.BAD_REQUEST),
            dict(
                status=HTTPStatus.BAD_REQUEST,
            ),
        ),
    ],
)
async def test_route_put_extracted_data__different_services_available__success(
    client, corleone_params, extraction_params, expected_params, explanation
):
    with aioresponses() as mock_response:
        mock_response.put(CORLEONE_EXTRACTED_DATA_FIELD_URL, **corleone_params)
        mock_response.put(EXTRACTION_EXTRACTED_DATA_FIELD_URL, **extraction_params)

        res = await client.put(
            f"{EXTRACTED_DATA_URL}/111/field", headers=HEADERS, json=EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON
        )
    assert res.status_code == expected_params["status"]
    if expected_response := expected_params.get("payload"):
        assert res.json() == expected_response, explanation


@pytest.fixture()
def mocked_update_extracted_data_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.mark.asyncio
async def test_route_update_extracted_data__both_services_available__successful(
    client,
    mocked_update_extracted_data_request,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    res = await client.put(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS, json=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_update_extracted_data__both_services_unavailable__error(client, document_type_source_cache):
    document_type_source_cache.clear()

    res = await client.put(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS, json=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "corleone_response, extraction_response",
    [
        (
            {
                "content": EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            Exception,
            {
                "content": EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_route_update_extracted_data__one_of_services_unavailable__success(
    client, mocked_update_extracted_data_request, corleone_response, extraction_response, document_type_source_cache
):
    document_type_source_cache.clear()

    mocked_update_extracted_data_request.side_effect = [corleone_response, extraction_response]
    res = await client.put(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS, json=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON)

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_route_update_extracted_data__document_type_from_corleone__successful(
    client,
    mocked_update_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "corleone_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    res = await client.put(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS, json=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_update_extracted_data__document_type_from_corleone__error(
    client,
    mocked_update_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "corleone_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_update_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.put(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS, json=EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_route_update_extracted_data__document_type_from_type__successful(
    client,
    mocked_update_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "doc_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_update_extracted_data_request.side_effect = [
        {
            "content": EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]

    res = await client.put(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS, json=EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_update_extracted_data__document_type_from_type__error(
    client,
    mocked_update_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "doc_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_update_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.put(f"{EXTRACTED_DATA_URL}/1", headers=HEADERS, json=EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_route_field_chunk__both_services_available__successful(
    client,
    mocked_field_chunk_request,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    res = await client.get(f"{EXTRACTED_DATA_URL}/1/fields/1/chunk", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_field_chunk__both_services_unavailable__error(client):
    res = await client.get(f"{EXTRACTED_DATA_URL}/1/fields/1/chunk", headers=HEADERS)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "extraction_response, corleone_response",
    [
        (
            {
                "content": CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            Exception,
            {
                "content": CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_route_field_chunk__one_of_services_unavailable__success(
    client, mocked_field_chunk_request, corleone_response, extraction_response, document_type_source_cache
):
    document_type_source_cache.clear()

    mocked_extracted_data_request.side_effect = [corleone_response, extraction_response]
    res = await client.get(f"{EXTRACTED_DATA_URL}/1/fields/1/chunk", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_route_field_chunk__document_type_from_corleone__successful(
    client,
    mocked_field_chunk_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}/fields/{document_type_code}/chunk", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_field_chunk__document_type_from_corleone__error(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}/fields/{document_type_code}/chunk", headers=HEADERS)

    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_route_field_chunk__document_type_from_type__successful(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_extracted_data_request.side_effect = [
        {
            "content": CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}/fields/{document_type_code}/chunk", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_field_chunk__document_type_from_type__error(
    client,
    mocked_extracted_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "qwerty"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_extracted_data_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{EXTRACTED_DATA_URL}/{document_id}/fields/{document_type_code}/chunk", headers=HEADERS)

    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.fixture()
def mocked_update_extracted_data_cells_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.mark.asyncio
async def test_route_update_extracted_data_cells__both_services_available__successful(
    client,
    mocked_update_extracted_data_cells_request,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    res = await client.patch(
        f"{EXTRACTED_DATA_URL}/1/fields/2", headers=HEADERS, json=EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_update_extracted_data_cells__both_services_unavailable__error(
    client,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    res = await client.patch(
        f"{EXTRACTED_DATA_URL}/1/fields/2", headers=HEADERS, json=EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "corleone_response, extraction_response",
    [
        (
            {
                "content": EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            Exception,
            {
                "content": EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_route_update_extracted_data_cells__one_of_services_unavailable__success(
    client,
    mocked_update_extracted_data_cells_request,
    corleone_response,
    extraction_response,
    document_type_source_cache,
):
    document_type_source_cache.clear()

    mocked_update_extracted_data_cells_request.side_effect = [corleone_response, extraction_response]
    res = await client.patch(
        f"{EXTRACTED_DATA_URL}/1/fields/2", headers=HEADERS, json=EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON
    )

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_route_update_extracted_data_cells__document_type_from_corleone__successful(
    client,
    mocked_update_extracted_data_cells_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "corleone_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    res = await client.patch(
        f"{EXTRACTED_DATA_URL}/{document_id}/fields/2",
        headers=HEADERS,
        json=EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_update_extracted_data_cells__document_type_from_corleone__error(
    client,
    mocked_update_extracted_data_cells_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "corleone_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_update_extracted_data_cells_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.patch(
        f"{EXTRACTED_DATA_URL}/{document_id}/fields/2",
        headers=HEADERS,
        json=EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_route_update_extracted_data_cells__document_type_from_type__successful(
    client,
    mocked_update_extracted_data_cells_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "doc_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_update_extracted_data_cells_request.side_effect = [
        {
            "content": EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]
    res = await client.patch(
        f"{EXTRACTED_DATA_URL}/{document_id}/fields/2",
        headers=HEADERS,
        json=EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json() == EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON


@pytest.mark.asyncio
async def test_route_update_extracted_data_cells__document_type_from_type__error(
    client,
    mocked_update_extracted_data_cells_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = "doc_type"
    document_id = 1

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_update_extracted_data_cells_request.side_effect = [
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
        {
            "content": "",
            "status_code": 404,
            "headers": HEADERS,
        },
    ]

    res = await client.patch(
        f"{EXTRACTED_DATA_URL}/{document_id}/fields/2",
        headers=HEADERS,
        json=EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
