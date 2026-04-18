from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    EXTRACTION_BASE_API_PREFIX,
    TEMPLATE_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from tests.data.extraction_json_data import *
from tests.data.template_json_data import *

TEMPLATE_BASE_URL = f"{TEMPLATE_BASE_API_PREFIX}{V1_PREFIX}/templates"
EXTRACTION_V2_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}"
EXTRACTION_V1_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}"
HEADERS = {"deps-token": '{"organisation": "deps-users"}'}


@pytest.mark.asyncio
@pytest.mark.template
async def test_template_route__create_template_field__created(client, template_id: str):
    template_url = f"{TEMPLATE_BASE_URL}/{template_id}/fields"
    extraction_url = f"{EXTRACTION_V2_BASE_URL}/document-types/{template_id}/extraction-fields"

    with aioresponses() as mock_response:
        mock_response.post(
            extraction_url,
            status=HTTPStatus.CREATED,
            body=EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
        )

        response = await client.post(
            template_url,
            json=TEMPLATE_FIELD_CREATE_REQUEST_DICT,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert json.loads(response.content) == EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT


@pytest.mark.asyncio
@pytest.mark.template
async def test_template_route__update_template_field__updated(client, template_id: str):
    field_code = "test_field_code"
    template_url = f"{TEMPLATE_BASE_URL}/{template_id}/fields"
    extraction_url = f"{EXTRACTION_V2_BASE_URL}/document-types/{template_id}/extraction-fields/{field_code}"

    with aioresponses() as mock_response:
        mock_response.patch(
            extraction_url,
            status=HTTPStatus.OK,
            body=EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
        )

        response = await client.patch(
            f"{template_url}/{field_code}",
            json=TEMPLATE_FIELD_UPDATE_REQUEST_DICT,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.template
async def test_template_route__delete_template_field__deleted(client, template_id: str):
    field_code = "test_field_code"
    template_url = f"{TEMPLATE_BASE_URL}/{template_id}/fields"
    extraction_url = f"{EXTRACTION_V2_BASE_URL}/document-types/{template_id}/extraction-fields?fieldCodes={field_code}"

    with aioresponses() as mock_response:
        mock_response.delete(
            extraction_url,
            status=HTTPStatus.NO_CONTENT,
        )
        response = await client.delete(
            f"{template_url}/{field_code}",
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.template
async def test_route_get_template_fields(client, template_id: str):
    template_url = f"{TEMPLATE_BASE_URL}/{template_id}/fields"
    extraction_url = f"{EXTRACTION_V1_BASE_URL}/document-types/{template_id}"

    with aioresponses() as mock_response:
        mock_response.get(
            extraction_url,
            status=HTTPStatus.OK,
            body=DOCUMENT_TYPE_WITH_TEMPLATE_FIELDS_RESPONSE_JSON,
        )

        response = await client.get(
            template_url,
            headers=HEADERS,
        )

        assert response.status_code == HTTPStatus.OK

        TEMPLATE_FIELDS_RESPONSE_LIST[0]["templateId"] = template_id

        assert json.loads(response.content) == TEMPLATE_FIELDS_RESPONSE_LIST
