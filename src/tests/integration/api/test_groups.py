import copy
import json
import urllib
from datetime import datetime
from http import HTTPStatus
from typing import Any, Optional
from urllib.parse import urlencode

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.application.group import GetGroupExtras
from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    CLASSIFICATION_BASE_API_PREFIX,
    GROUPS_BASE_API_PREFIX,
    SPLITTING_BASE_API_PREFIX,
    V1_PREFIX,
)
from tests.data.groups_json_data import *
from tests.data.splitter_json_data import (
    FIND_ALL_SPLITTERS_RESPONSE,
    FIND_SPLITTERS_RESPONSE,
)

API_GATEWAY_GROUPS_V5_URL = f"{BASE_API_V5_PREFIX}/groups"
GROUPS_BASE_V1_URL = f"{GROUPS_BASE_API_PREFIX}{V1_PREFIX}/groups"
CLASSIFICATION_BASE_URL = f"{CLASSIFICATION_BASE_API_PREFIX}{V1_PREFIX}"
SPLITTING_SERVICE_SPLITTERS_URL = f"{SPLITTING_BASE_API_PREFIX}{V1_PREFIX}/splitters"


@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_groups__ok(client: AsyncClient):
    params = {
        "name": "",
        "page": 0,
        "perPage": 2,
        "sortBy": "created_at",
        "sortOrder": "asc",
    }

    groups = {
        "meta": {"total": 5, "size": 2},
        "result": [
            {
                "id": "1",
                "name": "1",
                "documentTypeIds": ["1", "2", "3"],
                "createdAt": str(datetime.now()),
            },
            {
                "id": "2",
                "name": "2",
                "documentTypeIds": ["1", "3"],
                "createdAt": str(datetime.now()),
            },
        ],
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{GROUPS_BASE_V1_URL}?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.OK,
            body=json.dumps(groups),
        )

        response = await client.get(API_GATEWAY_GROUPS_V5_URL, params=params)
        mock_response.assert_called_once()

        assert response.status_code == HTTPStatus.OK
        assert response.json() == groups


@pytest.mark.asyncio
@pytest.mark.groups
async def test_create_group__ok(client: AsyncClient):
    data = {"name": "test", "documentTypeIds": ["1", "3"]}

    group = {
        "id": "2148294",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            GROUPS_BASE_V1_URL,
            status=HTTPStatus.CREATED,
            body=json.dumps(group),
        )

        response = await client.post(API_GATEWAY_GROUPS_V5_URL, json=data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == group


@pytest.mark.asyncio
@pytest.mark.groups
async def test_delete_group__ok(client: AsyncClient):
    params = {"id": ["1", "2", "3"]}

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{GROUPS_BASE_V1_URL}?{urlencode(params, doseq=True)}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(API_GATEWAY_GROUPS_V5_URL, params=params)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.parametrize(
    "extras",
    (
        [GetGroupExtras.CLASSIFIERS.value],
        None,
    ),
)
@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_group__ok(client: AsyncClient, group_id: str, extras: Optional[list[GetGroupExtras]]):
    groups_url = f"{GROUPS_BASE_V1_URL}/{group_id}"
    classification_url = f"{CLASSIFICATION_BASE_URL}/groups/{group_id}/gen-ai-classifiers"

    group: dict[str, Any] = copy.deepcopy(GET_GROUP_RESPONSE_DICT)
    group["group"]["genAiClassifiers"] = None
    group["group"]["splitters"] = None

    data = {}
    if extras is not None:
        data["extras"] = extras

        if GetGroupExtras.CLASSIFIERS in extras:
            group["group"]["genAiClassifiers"] = copy.deepcopy(GET_CLASSIFIERS_OF_GROUP_RESPONSE_DICT)[  # type: ignore
                "genAiClassifiers"
            ]

    with aioresponses() as mock_response:
        mock_response.get(groups_url, status=HTTPStatus.OK, body=GET_GROUP_RESPONSE_JSON)
        mock_response.get(classification_url, status=HTTPStatus.OK, body=GET_CLASSIFIERS_OF_GROUP_RESPONSE_JSON)

        response = await client.get(f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}", params=data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == group


@pytest.mark.asyncio
@pytest.mark.groups
async def test_update_group_info__ok(client: AsyncClient):
    data = {"name": "test"}

    group_id = "3284718"

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{GROUPS_BASE_V1_URL}/{group_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.patch(f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}", json=data)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.groups
async def test_add_document_types__ok(client: AsyncClient):
    data = {"documentTypeIds": ["1", "3", "5"]}

    group_id = "3284718"

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{GROUPS_BASE_V1_URL}/{group_id}/document-types",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.patch(f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}/document-types", json=data)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.groups
async def test_remove_document_types__ok(client: AsyncClient):
    params = {"id": ["1", "3", "5"]}

    group_id = "3284718"

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{GROUPS_BASE_V1_URL}/{group_id}/document-types?{urlencode(params, doseq=True)}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(
            f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}/document-types?{urlencode(params, doseq=True)}"
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.groups
async def test_create_gen_ai_classifier__created(client: AsyncClient, group_id: str, document_type_id: str):
    url = f"{CLASSIFICATION_BASE_URL}/gen-ai-classifiers"
    data = {
        "prompt": "prompt",
        "llmType": "llm",
        "name": "name",
    }

    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.CREATED, body=CREATE_GEN_AI_CLASSIFIER_RESPONSE_JSON)

        response = await client.post(
            f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}/document-types/{document_type_id}/gen-ai-classifiers",
            json=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CREATE_GEN_AI_CLASSIFIER_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.groups
async def test_update_gen_ai_classifier__no_content(client: AsyncClient, gen_ai_classifier_id: str):
    url = f"{CLASSIFICATION_BASE_URL}/gen-ai-classifiers/{gen_ai_classifier_id}"
    data = {
        "prompt": "prompt",
        "llmType": "llm",
        "name": "name",
    }

    with aioresponses() as mock_response:
        mock_response.patch(url, status=HTTPStatus.NO_CONTENT)

        response = await client.patch(
            f"{API_GATEWAY_GROUPS_V5_URL}/gen-ai-classifiers/{gen_ai_classifier_id}",
            json=data,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.groups
async def test_delete_gen_ai_classifiers__no_content(client: AsyncClient, gen_ai_classifier_id: str):
    params = {"id": [gen_ai_classifier_id]}
    url = f"{CLASSIFICATION_BASE_URL}/gen-ai-classifiers?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.delete(url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(f"{API_GATEWAY_GROUPS_V5_URL}/gen-ai-classifiers", params=params)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_classifiers_of_group__ok(client: AsyncClient, group_id: str):
    url = f"{CLASSIFICATION_BASE_URL}/groups/{group_id}/gen-ai-classifiers"

    with aioresponses() as mock_response:
        mock_response.get(url, body=GET_CLASSIFIERS_OF_GROUP_RESPONSE_JSON)

        response = await client.get(f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}/classifiers")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_CLASSIFIERS_OF_GROUP_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_group_splitters__ok(client: AsyncClient, group_id: str):
    params = {"groupId": group_id}

    with aioresponses() as mock_response:
        mock_response.get(
            f"{SPLITTING_SERVICE_SPLITTERS_URL}?{urllib.parse.urlencode(params)}",
            status=HTTPStatus.OK,
            payload=FIND_SPLITTERS_RESPONSE,
        )

        response = await client.get(f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}/splitters")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == FIND_SPLITTERS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_groups__with_splittings__splitter_with_null_document_type_id__splitter_matched_to_group(
    client: AsyncClient,
):
    groups_params = {"sortBy": "createdAt", "sortOrder": "desc"}
    groups_url = f"{GROUPS_BASE_V1_URL}?{urllib.parse.urlencode(groups_params)}"
    created_at = str(datetime.now())
    groups_data = {
        "meta": {"total": 1, "size": 1},
        "result": [{"id": "group-id-1", "name": "Group 1", "documentTypeIds": [], "createdAt": created_at}],
    }

    with aioresponses() as mock_response:
        mock_response.get(groups_url, status=HTTPStatus.OK, payload=groups_data)
        mock_response.get(SPLITTING_SERVICE_SPLITTERS_URL, status=HTTPStatus.OK, payload=FIND_ALL_SPLITTERS_RESPONSE)

        response = await client.get(API_GATEWAY_GROUPS_V5_URL, params={"extras": "splitters"})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"][0]["splitter"] == FIND_ALL_SPLITTERS_RESPONSE["splitters"][0]  # type: ignore


@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_groups__with_splittings__splitter_has_document_type_id__splitter_not_matched(
    client: AsyncClient,
):
    groups_params = {"sortBy": "createdAt", "sortOrder": "desc"}
    groups_url = f"{GROUPS_BASE_V1_URL}?{urllib.parse.urlencode(groups_params)}"
    created_at = str(datetime.now())
    groups_data = {
        "meta": {"total": 1, "size": 1},
        "result": [{"id": "group-id-2", "name": "Group 2", "documentTypeIds": [], "createdAt": created_at}],
    }

    with aioresponses() as mock_response:
        mock_response.get(groups_url, status=HTTPStatus.OK, payload=groups_data)
        mock_response.get(SPLITTING_SERVICE_SPLITTERS_URL, status=HTTPStatus.OK, payload=FIND_ALL_SPLITTERS_RESPONSE)

        response = await client.get(API_GATEWAY_GROUPS_V5_URL, params={"extras": "splitters"})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"][0]["splitter"] is None


@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_groups__with_splittings__no_matching_group__splitter_is_null(
    client: AsyncClient,
):
    groups_params = {"sortBy": "createdAt", "sortOrder": "desc"}
    groups_url = f"{GROUPS_BASE_V1_URL}?{urllib.parse.urlencode(groups_params)}"
    created_at = str(datetime.now())
    groups_data = {
        "meta": {"total": 1, "size": 1},
        "result": [{"id": "group-id-99", "name": "Group 99", "documentTypeIds": [], "createdAt": created_at}],
    }

    with aioresponses() as mock_response:
        mock_response.get(groups_url, status=HTTPStatus.OK, payload=groups_data)
        mock_response.get(SPLITTING_SERVICE_SPLITTERS_URL, status=HTTPStatus.OK, payload=FIND_ALL_SPLITTERS_RESPONSE)

        response = await client.get(API_GATEWAY_GROUPS_V5_URL, params={"extras": "splitters"})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["result"][0]["splitter"] is None


@pytest.mark.asyncio
@pytest.mark.groups
async def test_get_group_with_splitters_extra__ok(client: AsyncClient, group_id: str):
    groups_url = f"{GROUPS_BASE_V1_URL}/{group_id}"
    splitters_url = f"{SPLITTING_SERVICE_SPLITTERS_URL}?{urllib.parse.urlencode({'groupId': group_id})}"

    group: dict[str, Any] = copy.deepcopy(GET_GROUP_RESPONSE_DICT)
    group["group"]["genAiClassifiers"] = None
    group["group"]["splitters"] = FIND_SPLITTERS_RESPONSE["splitters"]

    with aioresponses() as mock_response:
        mock_response.get(groups_url, status=HTTPStatus.OK, body=GET_GROUP_RESPONSE_JSON)
        mock_response.get(splitters_url, status=HTTPStatus.OK, payload=FIND_SPLITTERS_RESPONSE)

        response = await client.get(
            f"{API_GATEWAY_GROUPS_V5_URL}/{group_id}",
            params={"extras": GetGroupExtras.SPLITTERS.value},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == group
