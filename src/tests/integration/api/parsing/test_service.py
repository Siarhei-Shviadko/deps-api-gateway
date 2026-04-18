import json
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from deps_api_gateway.application import PageBatch, ParsingFeature, ParsingType
from deps_api_gateway.constants import (
    API_PREFIX,
    BASE_API_V5_PREFIX,
    DOCUMENT_ROUTER_PREFIX,
    FILES_ROUTER_PREFIX,
    PARSING_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from tests.data.parsing_json_data import (
    DOCUMENT_LAYOUT_JSON,
    EDIT_IMAGE_REQUEST_DICT,
    PARSING_INFO_JSON,
    TABULAR_LAYOUT_JSON,
)

PARSING_V1_URL = f"{PARSING_BASE_API_PREFIX}{V1_PREFIX}"
PARSING_V2_URL = f"{PARSING_BASE_API_PREFIX}{V2_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_get_document_layout_pages__ok(client, document_layout_id):
    params = {
        "batchIndex": PageBatch.index,
        "batchSize": PageBatch.size,
        "parsingType": ParsingType.AWS_TEXTRACT.value,
    }
    parsing_url = f"{PARSING_V1_URL}/document-layout/{document_layout_id}/pages?{urlencode(params, doseq=True)}"
    pages = []
    total = 0
    with aioresponses() as mock_response:
        mock_response.get(parsing_url, payload={"pages": pages, "total": total})

        response = await client.get(f"{API_PREFIX}/document-layout/{document_layout_id}/pages", params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "count": 0,
            "total": total,
            "next": (
                f"/api/api-gateway/v1/document-layout/{document_layout_id}/pages"
                "?parsingType=AWS_TEXTRACT&batchSize=1&batchIndex=1"
            ),
            "previous": "",
            "pages": pages,
        }


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_get_document_layout_pages__bad_request(client, document_layout_id):
    params = {
        "batchIndex": PageBatch.index,
        "batchSize": PageBatch.size,
        "parsingType": ParsingType.AWS_TEXTRACT.value,
    }
    parsing_url = f"{PARSING_V1_URL}/document-layout/{document_layout_id}/pages?{urlencode(params, doseq=True)}"
    with aioresponses() as mock_response:
        mock_response.get(parsing_url, status=HTTPStatus.BAD_REQUEST)

        response = await client.get(f"{API_PREFIX}/document-layout/{document_layout_id}/pages", params=params)

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_get_parsing_info__ok(client, document_id):
    parsing_url = f"{PARSING_V2_URL}/documents/{document_id}/parsing-info"
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/parsing-info"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, body=PARSING_INFO_JSON)

        response = await client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == json.loads(PARSING_INFO_JSON)


@pytest.mark.asyncio
async def test_get_parsing_info__service_unavailable__502_error(client, document_id):
    parsing_url = f"{PARSING_V2_URL}/documents/{document_id}/parsing-info"
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/parsing-info"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.get(url)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {"parsingType": ParsingType.AWS_TEXTRACT.value},
        {"parsingType": ParsingType.AWS_TEXTRACT.value, "features": ParsingFeature.IMAGES.value},
        {
            "batchIndex": 0,
            "batchSize": 1,
            "features": ParsingFeature.KEY_VALUE_PAIRS.value,
            "parsingType": ParsingType.AWS_TEXTRACT.value,
        },
    ],
)
async def test_get_document_layout_v2__ok(params, client, document_id):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/document-layout"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, body=DOCUMENT_LAYOUT_JSON)

        response = await client.get(url, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == json.loads(DOCUMENT_LAYOUT_JSON)


@pytest.mark.asyncio
async def test_get_document_layout__service_unavailable__502_error(client, document_id):
    params = {"parsingType": ParsingType.AWS_TEXTRACT.value}
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/document-layout"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.get(url, params=params)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
async def test_get_file_parsing_info__ok(client, file_id):
    parsing_url = f"{PARSING_V2_URL}/documents/{file_id}/parsing-info"
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/parsing-info"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, body=PARSING_INFO_JSON)

        response = await client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == json.loads(PARSING_INFO_JSON)


@pytest.mark.asyncio
async def test_get_file_parsing_info__service_unavailable__502_error(client, file_id):
    parsing_url = f"{PARSING_V2_URL}/documents/{file_id}/parsing-info"
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/parsing-info"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.get(url)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {"parsingType": ParsingType.AWS_TEXTRACT.value},
        {"parsingType": ParsingType.AWS_TEXTRACT.value, "features": ParsingFeature.IMAGES.value},
        {
            "batchIndex": 0,
            "batchSize": 1,
            "features": ParsingFeature.KEY_VALUE_PAIRS.value,
            "parsingType": ParsingType.AWS_TEXTRACT.value,
        },
        {
            "batchIndex": 5,
            "batchSize": 10,
            "parsingType": ParsingType.AWS_TEXTRACT.value,
        },
    ],
)
async def test_get_file_layout__ok(params, client, file_id):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/document-layout"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, body=DOCUMENT_LAYOUT_JSON)

        response = await client.get(url, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == json.loads(DOCUMENT_LAYOUT_JSON)


@pytest.mark.asyncio
async def test_get_file_layout__service_unavailable__502_error(client, file_id):
    params = {"parsingType": ParsingType.AWS_TEXTRACT.value}
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/document-layout"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.get(url, params=params)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params,expected_status",
    [
        ({"parsingType": ParsingType.AWS_TEXTRACT.value, "batchIndex": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"parsingType": ParsingType.AWS_TEXTRACT.value, "batchSize": 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"parsingType": ParsingType.AWS_TEXTRACT.value, "batchSize": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_get_file_layout__validation_error(params, expected_status, client, file_id):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/document-layout"

    response = await client.get(url, params=params)

    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {},
        {"tables": ["first_table", "second_table"]},
        {"rowSpan": (0, 0)},
        {"colSpan": (1, 1)},
        {"tables": ["first_table", "second_table"], "rowSpan": (0, 0), "colSpan": (1, 1)},
    ],
)
async def test_get_tabular_layout__ok(params, client, document_id):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/tabular-layout"
    parsing_url = f"{PARSING_V2_URL}/tabular-layout/{document_id}?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, body=TABULAR_LAYOUT_JSON)

        response = await client.get(url, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == json.loads(TABULAR_LAYOUT_JSON)
        mock_response.assert_called_once()
        assert [resp[0] for resp in mock_response.requests.values()][0].kwargs["params"] == params


@pytest.mark.asyncio
async def test_get_tabular_layout__service_unavailable__502_error(client, document_id):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/tabular-layout"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.get(url)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {},
        {"tables": ["first_table", "second_table"]},
        {"rowSpan": (0, 0)},
        {"colSpan": (1, 1)},
        {"tables": ["first_table", "second_table"], "rowSpan": (0, 0), "colSpan": (1, 1)},
    ],
)
async def test_get_file_tabular_layout__ok(params, client, file_id):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/tabular-layout"
    parsing_url = f"{PARSING_V2_URL}/tabular-layout/{file_id}?{urlencode(params, doseq=True)}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, body=TABULAR_LAYOUT_JSON)

        response = await client.get(url, params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == json.loads(TABULAR_LAYOUT_JSON)
        mock_response.assert_called_once()
        assert [resp[0] for resp in mock_response.requests.values()][0].kwargs["params"] == params


@pytest.mark.asyncio
async def test_get_file_tabular_layout__service_unavailable__502_error(client, file_id):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/tabular-layout"
    parsing_url = f"{PARSING_V2_URL}/tabular-layout/{file_id}"

    with aioresponses() as mock_response:
        mock_response.get(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.get(url)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
async def test_clone_document_layout__ok(client, document_id):
    url = f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/document-layout/user-parsing-type"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/user-parsing-type"
    payload = {"parsingType": "TESSERACT"}

    with aioresponses() as mock_response:
        mock_response.put(parsing_url, status=HTTPStatus.CREATED)

        response = await client.put(url, json=payload)

        assert response.status_code == HTTPStatus.CREATED
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_paragraph__200(
    update_paragraph_payload,
    paragraph_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/paragraphs/{paragraph_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/paragraphs/{paragraph_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=update_paragraph_payload)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_paragraph__404(
    update_paragraph_payload,
    paragraph_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/paragraphs/{paragraph_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/paragraphs/{paragraph_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.NOT_FOUND)

        response = await client.patch(url, json=update_paragraph_payload)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_paragraph__service_unavailable__502_error(
    update_paragraph_payload,
    paragraph_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/paragraphs/{paragraph_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/paragraphs/{paragraph_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.patch(url, json=update_paragraph_payload)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_image__ok(client, document_id) -> None:
    page_id = "pageId"
    img_id = "imageId"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/images/{img_id}"
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/images/{img_id}"
    )
    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=EDIT_IMAGE_REQUEST_DICT)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_table__200(
    update_table_payload,
    table_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/tables/{table_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/tables/{table_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=update_table_payload)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_table__404(
    update_table_payload,
    table_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/tables/{table_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/tables/{table_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.NOT_FOUND)

        response = await client.patch(url, json=update_table_payload)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_table__service_unavailable__502_error(
    update_table_payload,
    table_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/tables/{table_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/tables/{table_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.patch(url, json=update_table_payload)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_key_value_pair__200(
    update_key_value_pair_payload,
    key_value_pair_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/key-value-pairs/{key_value_pair_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/key-value-pairs/{key_value_pair_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=update_key_value_pair_payload)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_key_value_pair__404(
    update_key_value_pair_payload,
    key_value_pair_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/key-value-pairs/{key_value_pair_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/key-value-pairs/{key_value_pair_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.NOT_FOUND)

        response = await client.patch(url, json=update_key_value_pair_payload)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_key_value_pair__service_unavailable__502_error(
    update_key_value_pair_payload,
    key_value_pair_id,
    document_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{DOCUMENT_ROUTER_PREFIX}/{document_id}/"
        f"document-layout/pages/{page_id}/key-value-pairs/{key_value_pair_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{document_id}/pages/{page_id}/key-value-pairs/{key_value_pair_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.patch(url, json=update_key_value_pair_payload)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
async def test_clone_file_layout__ok(client, file_id):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/document-layout/user-parsing-type"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/user-parsing-type"
    payload = {"parsingType": "TESSERACT"}

    with aioresponses() as mock_response:
        mock_response.put(parsing_url, status=HTTPStatus.CREATED)

        response = await client.put(url, json=payload)

        assert response.status_code == HTTPStatus.CREATED
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_paragraph__200(
    update_paragraph_payload,
    paragraph_id,
    file_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/"
        f"document-layout/pages/{page_id}/paragraphs/{paragraph_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/paragraphs/{paragraph_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=update_paragraph_payload)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_paragraph__404(
    update_paragraph_payload,
    paragraph_id,
    file_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/"
        f"document-layout/pages/{page_id}/paragraphs/{paragraph_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/paragraphs/{paragraph_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.NOT_FOUND)

        response = await client.patch(url, json=update_paragraph_payload)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_paragraph__service_unavailable__502_error(
    update_paragraph_payload,
    paragraph_id,
    file_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/"
        f"document-layout/pages/{page_id}/paragraphs/{paragraph_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/paragraphs/{paragraph_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.patch(url, json=update_paragraph_payload)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_image__ok(client, file_id) -> None:
    page_id = "pageId"
    img_id = "imageId"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/images/{img_id}"
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/" f"document-layout/pages/{page_id}/images/{img_id}"
    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=EDIT_IMAGE_REQUEST_DICT)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_table__200(
    update_table_payload,
    table_id,
    file_id,
    page_id,
    client,
):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/" f"document-layout/pages/{page_id}/tables/{table_id}"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/tables/{table_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=update_table_payload)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_table__404(
    update_table_payload,
    table_id,
    file_id,
    page_id,
    client,
):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/" f"document-layout/pages/{page_id}/tables/{table_id}"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/tables/{table_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.NOT_FOUND)

        response = await client.patch(url, json=update_table_payload)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_table__service_unavailable__502_error(
    update_table_payload,
    table_id,
    file_id,
    page_id,
    client,
):
    url = f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/" f"document-layout/pages/{page_id}/tables/{table_id}"
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/tables/{table_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.patch(url, json=update_table_payload)

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_key_value_pair__200(
    update_key_value_pair_payload,
    key_value_pair_id,
    file_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/"
        f"document-layout/pages/{page_id}/key-value-pairs/{key_value_pair_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/key-value-pairs/{key_value_pair_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.OK)

        response = await client.patch(url, json=update_key_value_pair_payload)

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_key_value_pair__404(
    update_key_value_pair_payload,
    key_value_pair_id,
    file_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/"
        f"document-layout/pages/{page_id}/key-value-pairs/{key_value_pair_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/key-value-pairs/{key_value_pair_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, status=HTTPStatus.NOT_FOUND)

        response = await client.patch(url, json=update_key_value_pair_payload)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parsing
async def test_update_file_key_value_pair__service_unavailable__502_error(
    update_key_value_pair_payload,
    key_value_pair_id,
    file_id,
    page_id,
    client,
):
    url = (
        f"{BASE_API_V5_PREFIX}{FILES_ROUTER_PREFIX}/{file_id}/"
        f"document-layout/pages/{page_id}/key-value-pairs/{key_value_pair_id}"
    )
    parsing_url = f"{PARSING_V2_URL}/document-layout/{file_id}/pages/{page_id}/key-value-pairs/{key_value_pair_id}"

    with aioresponses() as mock_response:
        mock_response.patch(parsing_url, exception=ClientConnectionError("failed_connection"))

        response = await client.patch(url, json=update_key_value_pair_payload)

        assert response.status_code == HTTPStatus.BAD_GATEWAY
