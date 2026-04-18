from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import V1_PREFIX, VALIDATION_BASE_PREFIX
from tests.data.validation_json_data import (
    HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_JSON,
    HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT,
    HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON,
    VALIDATION_SERVICE_VALIDATION_RESULTS_NOT_FOUND_DICT,
    VALIDATION_SERVICE_VALIDATION_RESULTS_NOT_FOUND_JSON,
    VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_DICT,
    VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_JSON,
)

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}


@pytest.fixture
def mocked_validation_service_validation_results_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_JSON,
                "status_code": HTTPStatus.OK,
                "headers": HEADERS,
            }
        ],
    )
    mocker.patch(
        "deps_api_gateway.infrastructure.proxies.generic_rest_client.old.OldGenericRestClient.request",
        side_effect=async_mock,
    )
    return async_mock


@pytest.fixture
def mocked_high_sparrow_validation_results_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON,
                "status_code": HTTPStatus.OK,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(
        "deps_api_gateway.infrastructure.proxies.generic_rest_client.new.GenericRestClient.request",
        side_effect=async_mock,
    )
    return async_mock


@pytest.mark.asyncio
async def test_routing__get_validation_results__from_high_sparrow(
    client,
    document_id,
    mocked_high_sparrow_validation_results_request,
    mocked_validation_service_validation_results_request,
):
    url = f"{VALIDATION_BASE_PREFIX}{V1_PREFIX}/results/{document_id}"

    response = await client.get(url, headers=HEADERS)

    mocked_high_sparrow_validation_results_request.assert_called_once()
    mocked_validation_service_validation_results_request.assert_not_called()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "validation_service_response, expected_code, expected_content",
    [
        (
            {
                "content": VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_JSON,
                "status_code": HTTPStatus.OK,
                "headers": HEADERS,
            },
            HTTPStatus.OK,
            VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_DICT,
        ),
        (
            {
                "content": VALIDATION_SERVICE_VALIDATION_RESULTS_NOT_FOUND_JSON,
                "status_code": HTTPStatus.NOT_FOUND,
                "headers": HEADERS,
            },
            HTTPStatus.NOT_FOUND,
            VALIDATION_SERVICE_VALIDATION_RESULTS_NOT_FOUND_DICT,
        ),
    ],
    ids=["Validation OK", "Validation NOT_FOUND"],
)
async def test_routing__get_validation_results__from_validation_service(
    client,
    document_id,
    mocked_validation_service_validation_results_request,
    mocked_high_sparrow_validation_results_request,
    validation_service_response,
    expected_code,
    expected_content,
):
    mocked_validation_service_validation_results_request.side_effect = [validation_service_response]
    mocked_high_sparrow_validation_results_request.side_effect = [
        {
            "content": HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_JSON,
            "status_code": HTTPStatus.NOT_FOUND,
            "headers": HEADERS,
        },
    ]
    url = f"{VALIDATION_BASE_PREFIX}{V1_PREFIX}/results/{document_id}"

    response = await client.get(url, headers=HEADERS)

    mocked_high_sparrow_validation_results_request.assert_called_once()
    mocked_validation_service_validation_results_request.assert_called_once()
    assert response.status_code == expected_code
    assert response.json() == expected_content


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "validation_service_response, high_sparrow_response, expected_code",
    [
        (
            {
                "content": VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_JSON,
                "status_code": HTTPStatus.OK,
                "headers": HEADERS,
            },
            Exception,
            HTTPStatus.OK,
        ),
        (
            Exception,
            {
                "content": HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON,
                "status_code": HTTPStatus.OK,
                "headers": HEADERS,
            },
            HTTPStatus.OK,
        ),
        (
            Exception,
            {
                "content": HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_JSON,
                "status_code": HTTPStatus.NOT_FOUND,
                "headers": HEADERS,
            },
            HTTPStatus.BAD_GATEWAY,
        ),
    ],
    ids=[
        "Validation OK | High sparrow ERROR",
        "Validation ERROR | High sparrow OK",
        "Validation ERROR | High sparrow NOT_FOUND",
    ],
)
async def test_routing__get_validation_results__one_service_unavailable(
    client,
    document_id,
    mocked_validation_service_validation_results_request,
    mocked_high_sparrow_validation_results_request,
    validation_service_response,
    high_sparrow_response,
    expected_code,
):
    mocked_validation_service_validation_results_request.side_effect = [validation_service_response]
    mocked_high_sparrow_validation_results_request.side_effect = [high_sparrow_response]
    url = f"{VALIDATION_BASE_PREFIX}{V1_PREFIX}/results/{document_id}"

    response = await client.get(url, headers=HEADERS)

    assert response.status_code == expected_code


@pytest.mark.asyncio
async def test_routing__get_validation_results__both_services_unavailable(
    client,
    document_id,
):
    url = f"{VALIDATION_BASE_PREFIX}{V1_PREFIX}/results/{document_id}"

    response = await client.get(url, headers=HEADERS)
    assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
async def test_routing__all_methods__called_router(client):
    url = f"{VALIDATION_BASE_PREFIX}{V1_PREFIX}/test"

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
