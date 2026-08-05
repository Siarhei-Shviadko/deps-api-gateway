import json
from http import HTTPStatus

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    SPLITTING_BASE_API_PREFIX,
    V1_PREFIX,
)
from tests.data.splitting_proposal_json_data import (
    GET_PROPOSAL_RESPONSE,
    UPDATE_PROPOSAL_REQUEST,
)

GATEWAY_PROPOSALS_URL = f"{BASE_API_V5_PREFIX}/splitting/splitting-proposals"
SPLITTING_SERVICE_PROPOSALS_URL = f"{SPLITTING_BASE_API_PREFIX}{V1_PREFIX}/splitting-proposals"


@pytest.mark.asyncio
@pytest.mark.splitting_proposals
async def test_get_proposal__ok(client: AsyncClient, faker):
    proposal_id = faker.uuid4()

    with aioresponses() as mock:
        mock.get(
            f"{SPLITTING_SERVICE_PROPOSALS_URL}/{proposal_id}",
            status=HTTPStatus.OK,
            body=json.dumps(GET_PROPOSAL_RESPONSE),
        )

        response = await client.get(f"{GATEWAY_PROPOSALS_URL}/{proposal_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_PROPOSAL_RESPONSE


@pytest.mark.asyncio
@pytest.mark.splitting_proposals
async def test_get_proposal__not_found(client: AsyncClient, faker):
    proposal_id = faker.uuid4()
    body = {"code": "proposal_not_found", "message": "Proposal not found"}

    with aioresponses() as mock:
        mock.get(
            f"{SPLITTING_SERVICE_PROPOSALS_URL}/{proposal_id}",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(body),
        )

        response = await client.get(f"{GATEWAY_PROPOSALS_URL}/{proposal_id}")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.splitting_proposals
async def test_update_proposal__ok(client: AsyncClient, faker):
    proposal_id = faker.uuid4()

    with aioresponses() as mock:
        mock.patch(
            f"{SPLITTING_SERVICE_PROPOSALS_URL}/{proposal_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.patch(f"{GATEWAY_PROPOSALS_URL}/{proposal_id}", json=UPDATE_PROPOSAL_REQUEST)

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.splitting_proposals
async def test_update_proposal__not_found(client: AsyncClient, faker):
    proposal_id = faker.uuid4()
    body = {"code": "proposal_not_found", "message": "Proposal not found"}

    with aioresponses() as mock:
        mock.patch(
            f"{SPLITTING_SERVICE_PROPOSALS_URL}/{proposal_id}",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(body),
        )

        response = await client.patch(f"{GATEWAY_PROPOSALS_URL}/{proposal_id}", json=UPDATE_PROPOSAL_REQUEST)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body


@pytest.mark.asyncio
@pytest.mark.splitting_proposals
async def test_confirm_proposal__ok(client: AsyncClient, faker):
    proposal_id = faker.uuid4()

    with aioresponses() as mock:
        mock.post(
            f"{SPLITTING_SERVICE_PROPOSALS_URL}/{proposal_id}/confirm",
            status=HTTPStatus.ACCEPTED,
        )

        response = await client.post(f"{GATEWAY_PROPOSALS_URL}/{proposal_id}/confirm")

        assert response.status_code == HTTPStatus.ACCEPTED


@pytest.mark.asyncio
@pytest.mark.splitting_proposals
async def test_confirm_proposal__not_found(client: AsyncClient, faker):
    proposal_id = faker.uuid4()
    body = {"code": "proposal_not_found", "message": "Proposal not found"}

    with aioresponses() as mock:
        mock.post(
            f"{SPLITTING_SERVICE_PROPOSALS_URL}/{proposal_id}/confirm",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(body),
        )

        response = await client.post(f"{GATEWAY_PROPOSALS_URL}/{proposal_id}/confirm")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == body
