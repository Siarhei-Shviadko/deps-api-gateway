from http import HTTPStatus
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    PREPROCESS_BASE_API_PREFIX,
    V1_PREFIX,
    DocumentTypeSource,
)
from tests.data.json_data import (
    RESPONSE_FORM_PREPROCESS_JSON,
    RESPONSE_FORM_PREPROCESS_TABLE_CELLS_RAW,
    RESPONSE_FORM_UNIFIER_JSON,
    RESPONSE_FORM_UNIFIER_RAW,
    RESPONSE_FORM_UNIFIER_TABLE_CELLS_JSON,
    RESPONSE_FORM_UNIFIER_TABLE_CELLS_RAW,
    RESPONSE_FROM_PREPROCESS_RAW,
)

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}
UNIFIED_DATA_URL = f"{PREPROCESS_BASE_API_PREFIX}{V1_PREFIX}/unified_data/deprecated"
TABLE_CELLS_URL = f"{PREPROCESS_BASE_API_PREFIX}{V1_PREFIX}/preprocessed-table-data"


@pytest.fixture
def mocked_unified_data_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": RESPONSE_FROM_PREPROCESS_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": RESPONSE_FORM_UNIFIER_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(
        "deps_api_gateway.infrastructure.proxies.generic_rest_client.old.OldGenericRestClient.request",
        side_effect=async_mock,
    )
    return async_mock


@pytest.fixture
def mocked_unified_table_cells_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": RESPONSE_FORM_PREPROCESS_TABLE_CELLS_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": RESPONSE_FORM_UNIFIER_TABLE_CELLS_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(
        "deps_api_gateway.infrastructure.proxies.generic_rest_client.old.OldGenericRestClient.request",
        side_effect=async_mock,
    )
    return async_mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mocked_request_fixture, url, expected",
    [
        (
            "mocked_unified_data_request",
            f"{UNIFIED_DATA_URL}/{RESPONSE_FORM_UNIFIER_JSON['documentId']}",
            RESPONSE_FORM_UNIFIER_JSON,
        ),
        (
            "mocked_unified_table_cells_request",
            f"{TABLE_CELLS_URL}/1/{uuid4().hex}",
            RESPONSE_FORM_UNIFIER_TABLE_CELLS_JSON,
        ),
    ],
)
async def test_routing__get_unified_data__both_services_available__successful(
    client,
    document_type_code_cache,
    mocked_request_fixture,
    url,
    expected,
    request,
):
    request.getfixturevalue(mocked_request_fixture)
    document_type_code_cache.clear()

    res = await client.get(url, headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url",
    [
        f"{UNIFIED_DATA_URL}/{RESPONSE_FORM_UNIFIER_JSON['documentId']}",
        f"{TABLE_CELLS_URL}/1/{uuid4().hex}",
    ],
)
async def test_routing__get_unified_data__both_services_unavailable__error(
    client,
    document_type_code_cache,
    url,
):
    document_type_code_cache.clear()

    res = await client.get(url, headers=HEADERS)

    assert res.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mocked_request_fixture, url, preprocess_response, unifier_response",
    [
        (
            "mocked_unified_data_request",
            f"{UNIFIED_DATA_URL}/{RESPONSE_FORM_UNIFIER_JSON['documentId']}",
            {
                "content": RESPONSE_FROM_PREPROCESS_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            "mocked_unified_data_request",
            f"{UNIFIED_DATA_URL}/{RESPONSE_FORM_UNIFIER_JSON['documentId']}",
            Exception,
            {
                "content": RESPONSE_FORM_UNIFIER_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
        (
            "mocked_unified_table_cells_request",
            f"{TABLE_CELLS_URL}/1/{uuid4().hex}",
            {
                "content": RESPONSE_FORM_PREPROCESS_TABLE_CELLS_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            Exception,
        ),
        (
            "mocked_unified_table_cells_request",
            f"{TABLE_CELLS_URL}/1/{uuid4().hex}",
            Exception,
            {
                "content": RESPONSE_FORM_UNIFIER_TABLE_CELLS_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ),
    ],
)
async def test_routing__get_unified_data__one_of_services_unavailable__successful(
    client,
    document_type_code_cache,
    mocked_request_fixture,
    url,
    preprocess_response,
    unifier_response,
    request,
):
    request.getfixturevalue(mocked_request_fixture)
    document_type_code_cache.clear()

    mocked_unified_data_request.side_effect = [preprocess_response, unifier_response]
    res = await client.get(url, headers=HEADERS)

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_routing__get_unified_data__document_type_from_corleone__successful(
    client,
    mocked_unified_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = uuid4().hex
    document_id = RESPONSE_FORM_PREPROCESS_JSON["documentId"]

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    res = await client.get(f"{UNIFIED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == RESPONSE_FORM_PREPROCESS_JSON


@pytest.mark.asyncio
async def test_routing__get_unified_data__document_type_from_corleone__error(
    client,
    mocked_unified_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = uuid4().hex
    document_id = RESPONSE_FORM_PREPROCESS_JSON["documentId"]

    document_type_source_cache[document_type_code] = DocumentTypeSource.CORLEONE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_unified_data_request.side_effect = [
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

    res = await client.get(f"{UNIFIED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_routing__get_unified_data__document_type_from_type__successful(
    client,
    mocked_unified_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = uuid4().hex
    document_id = RESPONSE_FORM_UNIFIER_JSON["documentId"]

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_unified_data_request.side_effect = [
        {
            "content": RESPONSE_FORM_UNIFIER_RAW,
            "status_code": 200,
            "headers": HEADERS,
        },
        {
            "content": RESPONSE_FORM_PREPROCESS_JSON,
            "status_code": 200,
            "headers": HEADERS,
        },
    ]

    res = await client.get(f"{UNIFIED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == RESPONSE_FORM_UNIFIER_JSON


@pytest.mark.asyncio
async def test_routing__get_unified_data__document_type_from_type__error(
    client,
    mocked_unified_data_request,
    document_type_source_cache,
    document_type_code_cache,
):
    document_type_code = uuid4().hex
    document_id = RESPONSE_FORM_UNIFIER_JSON["documentId"]

    document_type_source_cache[document_type_code] = DocumentTypeSource.DOCUMENT_TYPE
    document_type_code_cache[str(document_id)] = document_type_code

    mocked_unified_data_request.side_effect = [
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

    res = await client.get(f"{UNIFIED_DATA_URL}/{document_id}", headers=HEADERS)

    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_routing__all_methods__called_router(client):
    url = f"{PREPROCESS_BASE_API_PREFIX}{V1_PREFIX}/test"

    with aioresponses() as mocked:
        for attempt, (mock, request) in enumerate(
            zip(
                (mocked.get, mocked.post, mocked.put, mocked.delete, mocked.patch),
                (client.get, client.post, client.put, client.delete, client.patch),
            ),
            1,
        ):
            mock(url)
            await request(url, headers=HEADERS)

            assert attempt == len(mocked.requests)
