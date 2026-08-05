import aiohttp
import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import BASE_API_V5_PREFIX
from tests.data.litellm_json_data import (
    LITELLM_MODELS_RESPONSE_DICT,
    LITELLM_MODELS_RESPONSE_JSON,
)


@pytest.mark.asyncio
@pytest.mark.litellm
async def test_get_litellm_models__ok__returns_models(client):
    with aioresponses() as mock_response:
        mock_response.get("/models", body=LITELLM_MODELS_RESPONSE_JSON, status=200)

        response = await client.get(f"{BASE_API_V5_PREFIX}/litellm/models")

        assert response.status_code == 200
        assert response.json() == LITELLM_MODELS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.litellm
async def test_get_litellm_models__upstream_unavailable__returns_error(client):
    with aioresponses() as mock_response:
        mock_response.get("/models", exception=aiohttp.ClientConnectionError())

        response = await client.get(f"{BASE_API_V5_PREFIX}/litellm/models")

        assert response.status_code >= 400
