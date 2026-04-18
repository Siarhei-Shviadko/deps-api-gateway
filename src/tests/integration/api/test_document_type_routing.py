from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    DOCUMENT_TYPE_BASE_API_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from tests.data.document_type_json_data import *

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}


@pytest.mark.asyncio
async def test_routing__attach_template_extractor_v1__successful(client):
    document_type_url = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/types"
    extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/attach-extractor"
    DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE["extractorType"] = "template"

    with aioresponses() as mocked:
        mocked.post(
            extraction_url, status=HTTPStatus.CREATED, body=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE)
        )

        response = await client.post(document_type_url, data=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_REQUEST))

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE


@pytest.mark.asyncio
async def test_routing__attach_non_extractor_v2__successful(client):
    document_type_url = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V2_PREFIX}/types"
    extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/attach-extractor"
    DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE["extractorType"] = "non"

    with aioresponses() as mocked:
        mocked.post(
            extraction_url, status=HTTPStatus.CREATED, body=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE)
        )

        response = await client.post(document_type_url, data=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_REQUEST))

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE


@pytest.mark.asyncio
async def test_routing__attach_prototype_extractor_v1__successful(client):
    document_type_url = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/types/prototype"
    extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/attach-extractor"
    DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE["extractorType"] = "prototype"

    with aioresponses() as mocked:
        mocked.post(
            extraction_url, status=HTTPStatus.CREATED, body=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE)
        )

        response = await client.post(document_type_url, data=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_REQUEST))

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE


@pytest.mark.asyncio
async def test_routing__attach_plugin_extractor__successful(client):
    document_type_url = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/plugins/attach-extraction"
    extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/attach-extractor"

    with aioresponses() as mocked:
        mocked.post(
            extraction_url, status=HTTPStatus.CREATED, body=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE)
        )

        response = await client.put(document_type_url, data=json.dumps(DOCUMENT_TYPES_ATTACH_PLUGIN_EXTRACTOR_REQUEST))

        assert response.status_code == HTTPStatus.OK
        assert response.json() == DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE
