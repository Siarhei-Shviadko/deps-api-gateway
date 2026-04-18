from http import HTTPStatus
from uuid import uuid4

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    API_PREFIX,
    BASE_API_V5_PREFIX,
    V1_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)
from deps_api_gateway.infrastructure.proxies import (
    WorkflowManagerServiceUnavailableError,
)

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}


@pytest.mark.asyncio
async def test_old_endpoint__get_saga_state__valid_response(client):
    entity_id = uuid4().hex
    workflow_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/sagas/{entity_id}/state"
    with aioresponses() as mock_response:
        mock_response.get(workflow_url, body=b'"PROCESSING"')

        response = await client.get(f"{API_PREFIX}/sagas/{entity_id}/state", headers=HEADERS)

        assert response.status_code == HTTPStatus.OK
        assert response.content == b'"PROCESSING"'


@pytest.mark.asyncio
async def test_new_endpoint__get_saga_state__valid_response(client):
    entity_id = uuid4().hex
    workflow_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/sagas/{entity_id}/state"
    with aioresponses() as mock_response:
        mock_response.get(workflow_url, body=b'"PROCESSING"')

        response = await client.get(f"{BASE_API_V5_PREFIX}/sagas/{entity_id}/state", headers=HEADERS)

        assert response.status_code == HTTPStatus.OK
        assert response.content == b'"PROCESSING"'


@pytest.mark.asyncio
async def test_get_saga_state__service_unavailable(client):
    with aioresponses() as mock_response:
        mock_response.get(f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/sagas/{uuid4().hex}/state", status=500)

        response = await client.get(f"{BASE_API_V5_PREFIX}/sagas/{uuid4().hex}/state", headers=HEADERS)

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        assert WorkflowManagerServiceUnavailableError.code in response.content.decode()
