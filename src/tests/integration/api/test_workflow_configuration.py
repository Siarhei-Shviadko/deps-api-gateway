from http import HTTPStatus
from ipaddress import ip_address
from uuid import uuid4

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    V1_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)
from deps_api_gateway.infrastructure.proxies import (
    WorkflowManagerServiceUnavailableError,
)
from tests.data.workflow_manager_json_data import (
    WORKFLOW_CONFIGURATION_RESPONSE_DICT,
    WORKFLOW_CONFIGURATION_RESPONSE_JSON,
    WORKFLOW_CONFIGURATIONS_RESPONSE_DICT,
    WORKFLOW_CONFIGURATIONS_RESPONSE_JSON,
)


@pytest.mark.asyncio
async def test__get_workflow_configuration__valid_response(client):
    document_type_id = uuid4().hex
    workflow_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/workflow-configuration/{document_type_id}"
    with aioresponses() as mock_response:
        mock_response.get(workflow_url, body=WORKFLOW_CONFIGURATION_RESPONSE_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/workflow-configuration/{document_type_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == WORKFLOW_CONFIGURATION_RESPONSE_DICT


@pytest.mark.asyncio
async def test__get_workflow_configurations__valid_response(client):
    workflow_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/workflow-configuration"
    with aioresponses() as mock_response:
        mock_response.get(workflow_url, body=WORKFLOW_CONFIGURATIONS_RESPONSE_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/workflow-configuration")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == WORKFLOW_CONFIGURATIONS_RESPONSE_DICT


@pytest.mark.asyncio
async def test__get_workflow_configuration__service_unavailable(client):
    document_type_id = uuid4().hex
    workflow_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/workflow-configuration/{document_type_id}"
    with aioresponses() as mock_response:
        mock_response.get(workflow_url, status=HTTPStatus.BAD_GATEWAY)

        response = await client.get(f"{BASE_API_V5_PREFIX}/workflow-configuration/{document_type_id}")

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        assert WorkflowManagerServiceUnavailableError.code in response.content.decode()


@pytest.mark.asyncio
async def test__update_workflow_configuration__valid_response(client):
    document_type_id = uuid4().hex
    workflow_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/workflow-configuration"
    with aioresponses() as mock_response:
        mock_response.patch(workflow_url, body=WORKFLOW_CONFIGURATION_RESPONSE_JSON)

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/workflow-configuration/{document_type_id}", json=WORKFLOW_CONFIGURATION_RESPONSE_DICT
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == WORKFLOW_CONFIGURATION_RESPONSE_DICT
