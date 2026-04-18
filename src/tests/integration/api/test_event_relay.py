from http import HTTPStatus

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    EVENT_RELAY_BASE_API_PREFIX,
    EVENT_RELAY_ROUTER_PREFIX,
    V1_PREFIX,
)

EVENT_ROUTER_BASE_URL = f"{EVENT_RELAY_BASE_API_PREFIX}{V1_PREFIX}"
EVENT_ROUTER_API_GATEWAY_URL = f"{BASE_API_V5_PREFIX}{EVENT_RELAY_ROUTER_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.event_router
async def test_events_subscription__valid_events__subscribed(client: AsyncClient, prototype_id: str):
    events_url = f"{EVENT_ROUTER_BASE_URL}/stream"
    with aioresponses() as mock_response:
        mock_response.get(
            events_url,
            status=HTTPStatus.OK,
            payload=[{"chunk": 1}, {"chunk": 2}, {"chunk": 3}],
        )

        response = await client.get(f"{EVENT_ROUTER_API_GATEWAY_URL}/stream")
        assert response.status_code == HTTPStatus.OK
        assert response.content == b'[{"chunk": 1}, {"chunk": 2}, {"chunk": 3}]'


@pytest.mark.asyncio
@pytest.mark.event_router
async def test_events_subscription__no_connection__OK(client: AsyncClient, prototype_id: str):
    events_url = f"{EVENT_ROUTER_BASE_URL}/stream"
    with aioresponses() as mock_response:
        mock_response.get(
            events_url,
            status=HTTPStatus.FORBIDDEN,
        )
        response = await client.get(f"{EVENT_ROUTER_API_GATEWAY_URL}/stream")
        assert response.status_code == HTTPStatus.OK
        assert response.content == b""
