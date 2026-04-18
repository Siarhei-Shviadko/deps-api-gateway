import json
from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    OUTPUT_EXPORTING_BASE_PREFIX,
    V1_PREFIX,
)
from tests.data.output_exporting_json_data import (
    OUTPUT_PROFILE_RESPONSE_DICT,
    OUTPUT_PROFILE_RESPONSE_JSON,
    OUTPUTS_DICT,
    OUTPUTS_JSON,
)

OUTPUT_EXPORTING_BASE_URL = f"{OUTPUT_EXPORTING_BASE_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.output_exporting
async def test_get_outputs__ok(client, document_id):
    output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/document/{document_id}/outputs"
    with aioresponses() as mock_response:
        mock_response.get(output_exporting_url, body=OUTPUTS_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/outputs")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == OUTPUTS_DICT


@pytest.mark.asyncio
@pytest.mark.output_exporting
async def test_build_output__created(client, document_id, document_type_id, profile_id):
    output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/document/{document_id}/outputs"
    data = {
        "documentTypeId": document_type_id,
        "profileId": profile_id,
    }
    with aioresponses() as mock_response:
        mock_response.post(output_exporting_url, status=HTTPStatus.CREATED, body=OUTPUT_PROFILE_RESPONSE_JSON)

        response = await client.post(f"{BASE_API_V5_PREFIX}/documents/{document_id}/outputs", data=json.dumps(data))

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == OUTPUT_PROFILE_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.output_exporting
async def test_delete_output__no_content(client, document_id, output_id):
    output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/document/{document_id}/outputs/{output_id}"
    with aioresponses() as mock_response:
        mock_response.delete(output_exporting_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(f"{BASE_API_V5_PREFIX}/documents/{document_id}/outputs/{output_id}")

        assert response.status_code == HTTPStatus.NO_CONTENT
