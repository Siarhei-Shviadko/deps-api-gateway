from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    BASE_API_V1_PREFIX,
    PROMPTER_BASE_PREFIX,
    V1_PREFIX,
)
from tests.data.prompter_json_data import (
    PROMPTER_MODELS_DATA_DICT,
    PROMPTER_MODELS_DATA_JSON,
)

PROMPTER_BASE_URL = f"{PROMPTER_BASE_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.prompter
async def test_get_llms_with_codes__ok(client):
    prompter_url = f"{PROMPTER_BASE_URL}/extraction/models"
    with aioresponses() as mock_response:
        mock_response.get(prompter_url, body=PROMPTER_MODELS_DATA_JSON, status=HTTPStatus.OK)

        response = await client.get(f"{BASE_API_V1_PREFIX}/prompter/models")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == PROMPTER_MODELS_DATA_DICT
