import json
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from deps_api_gateway.application import Provider
from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    SEMANTIC_PARSING_BASE_API_PREFIX,
    V1_PREFIX,
)
from tests.data.parsing_json_data import SEMANTIC_LAYOUT_JSON

SEMANTIC_PARSING_V1_URL = f"{SEMANTIC_PARSING_BASE_API_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {},
        {"provider": Provider.LLAMAINDEX.value},
    ],
)
async def test_get_semantic_layout__ok(params, client, document_id):
    url = f"{BASE_API_V5_PREFIX}/semantic-layout/{document_id}"
    expected_params = params or {"provider": Provider.LLAMAINDEX.value}
    semantic_parsing_url = (
        f"{SEMANTIC_PARSING_V1_URL}/semantic-layout/{document_id}?{urlencode(expected_params, doseq=True)}"
    )

    with aioresponses() as mock_response:
        mock_response.get(semantic_parsing_url, body=SEMANTIC_LAYOUT_JSON)

        response = await client.get(url, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == json.loads(SEMANTIC_LAYOUT_JSON)
        mock_response.assert_called_once()
        assert [resp[0] for resp in mock_response.requests.values()][0].kwargs["params"] == expected_params


@pytest.mark.asyncio
async def test_get_semantic_layout__service_unavailable__502_error(client, document_id):
    params = {"provider": Provider.LLAMAINDEX.value}
    url = f"{BASE_API_V5_PREFIX}/semantic-layout/{document_id}"
    semantic_parsing_url = f"{SEMANTIC_PARSING_V1_URL}/semantic-layout/{document_id}?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.get(semantic_parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.get(url)

        assert response.status_code == HTTPStatus.BAD_GATEWAY
