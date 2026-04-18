from http import HTTPStatus

import pytest

from deps_api_gateway.constants import BASE_API_V5_PREFIX


@pytest.mark.asyncio
async def test_get_services__200(client):
    response = await client.get(f"{BASE_API_V5_PREFIX}/services")

    assert response.status_code == HTTPStatus.OK

    services = response.json()

    assert services["deployed"] == {
        "service_1": {"name": "Service 1"},
        "service_2": {"name": "Service 2"},
        "service_3": {"name": "Service 3"},
        "service_4": {"name": "Service 4"},
    }

    assert services["missed"] == {"service_5": {"name": "Service 5"}}
