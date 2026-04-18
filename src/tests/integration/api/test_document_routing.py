from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    CORLEONE_BASE_API_PREFIX,
    DOCUMENT_BASE_API_PREFIX,
    DOCUMENT_TYPE_BASE_API_PREFIX,
    PLUGIN_EXTRACTION_TYPE,
    V1_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
    DocumentTypeSource,
)
from tests.data.json_data import (
    RESPONSE_FROM_DOCUMENT_SERVICE_JSON,
    RESPONSE_FROM_DOCUMENT_SERVICE_RAW,
    TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
    UPLOAD_DOCUMENT_RESPONSE_RAW,
)

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}


@pytest.mark.asyncio
async def test_routing__get_documents__successful(client, document_type_code_cache):
    document_type_code_cache.clear()

    url = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents"
    with aioresponses() as mocked:
        mocked.get(url, status=200, body=RESPONSE_FROM_DOCUMENT_SERVICE_RAW)
        res = await client.get(url, headers=HEADERS)

        mocked.assert_called_once()
        assert res.status_code == HTTPStatus.OK
        assert res.json() == RESPONSE_FROM_DOCUMENT_SERVICE_JSON
        for document in RESPONSE_FROM_DOCUMENT_SERVICE_JSON["result"]:
            assert document["_id"] in document_type_code_cache


@pytest.mark.asyncio
async def test_routing__all_methods__called_router(client):
    url = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/test"

    with aioresponses() as mocked:
        for attempt, (mock, request) in enumerate(
            zip(
                (mocked.get, mocked.post, mocked.put, mocked.delete, mocked.patch),
                (client.get, client.post, client.put, client.delete, client.patch),
            ),
            1,
        ):
            mock(url)
            await request(url, headers=HEADERS)

            assert attempt == len(mocked.requests)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "type_source,extraction_type,result_body",
    [
        (DocumentTypeSource.CORLEONE, None, UPLOAD_DOCUMENT_RESPONSE_RAW),
        (DocumentTypeSource.DOCUMENT_TYPE, "plugin", ""),
        (DocumentTypeSource.DOCUMENT_TYPE, "template", ""),
        (DocumentTypeSource.DOCUMENT_TYPE, None, ""),
    ],
)
async def test_routing__upload_document__successful(
    client, document_type_source_cache, document_type_extraction_type_cache, type_source, extraction_type, result_body
):
    document_type_source_cache.clear()
    document_type_code = "test"
    document_type_source_cache[document_type_code] = type_source
    document_type_extraction_type_cache[document_type_code] = extraction_type

    url_documents = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/document-file"
    url_workflow = (
        f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/{extraction_type or PLUGIN_EXTRACTION_TYPE}-processing-workflow"
    )
    corleone_url = f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/types/{document_type_code}"
    document_type_url = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/types/{document_type_code}"

    with aioresponses() as mocked:
        mocked.post(url_documents, status=200, body=UPLOAD_DOCUMENT_RESPONSE_RAW)
        mocked.post(url_workflow, status=201, body="")
        mocked.get(corleone_url, status=200, body=TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON)
        mocked.get(document_type_url, status=200, body=TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON)

        res = await client.post(url_documents, headers=HEADERS, data={"documentType": document_type_code})

        mocked.assert_called()
        assert res.status_code in {HTTPStatus.OK, HTTPStatus.CREATED}
        assert res.text == result_body
