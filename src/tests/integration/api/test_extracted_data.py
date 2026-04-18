import json
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses
from async_rest_client.constants import Methods
from httpx import AsyncClient
from yarl import URL

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    V2_PREFIX,
)
from tests.data.extraction_json_data import (
    EXTRACTED_DATA_RESPONSE_DICT,
    EXTRACTED_DATA_RESPONSE_JSON,
    GET_TABLE_FIELD_CHUNK_RESPONSE_DICT,
    GET_TABLE_FIELD_CHUNK_RESPONSE_JSON,
    TABLE_FIELD_CHUNK_RESPONSE_DICT,
    TABLE_FIELD_CHUNK_RESPONSE_JSON,
)

EXTRACTION_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/extracted-data"


@pytest.mark.asyncio
async def test_get_extracted_data__ok(client: AsyncClient, document_id: str):
    data = {"rowsPerChunk": 15}

    url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/extracted-data/{document_id}?{urlencode(data)}"

    with aioresponses() as mock_response:
        mock_response.get(url, status=HTTPStatus.OK, body=EXTRACTED_DATA_RESPONSE_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data", params=data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == EXTRACTED_DATA_RESPONSE_DICT


@pytest.mark.asyncio
async def test_update_aliases__ok__204_status(client: AsyncClient, document_id, field_code):
    url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/extracted-data/{document_id}/fields/{field_code}/aliases"
    expected_payload = {"updatedAliases": {"elementd_id": "UpdatedValue"}}
    with aioresponses() as mock_response:
        mock_response.patch(url, status=HTTPStatus.NO_CONTENT)

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data/{field_code}/aliases",
            data=json.dumps(expected_payload),
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_response.assert_called_once()
        mock_response.requests.get((Methods.PATCH, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
async def test_update_aliases__not_found_error__400_status(client: AsyncClient, document_id, field_code):
    url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/extracted-data/{document_id}/fields/{field_code}/aliases"
    expected_payload = {"updatedAliases": {"elementd_id": "UpdatedValue"}}
    with aioresponses() as mock_response:
        mock_response.patch(url, status=HTTPStatus.BAD_REQUEST)

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data/{field_code}/aliases",
            data=json.dumps(expected_payload),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        mock_response.assert_called_once()
        mock_response.requests.get((Methods.PATCH, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
async def test_update_aliases__connection_error__502_status(client: AsyncClient, document_id, field_code):
    url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/extracted-data/{document_id}/fields/{field_code}/aliases"
    expected_payload = {"updatedAliases": {"elementd_id": "UpdatedValue"}}
    with aioresponses() as mock_response:
        mock_response.patch(url, exception=ClientConnectionError("failed_connection"))

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data/{field_code}/aliases",
            data=json.dumps(expected_payload),
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()
        mock_response.requests.get((Methods.PATCH, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
async def test_save_extracted_data__ok(client: AsyncClient, document_id: str):
    url = f"{EXTRACTION_BASE_URL}/{document_id}"
    data = {
        "fields": [
            {
                "fieldCode": "string",
                "data": {
                    "id": "string",
                    "value": "checked",
                    "confidence": -1,
                    "sourceBboxCoordinates": [{"sourceId": "string", "bboxes": [{"y": 0, "x": 0, "w": 0, "h": 0}]}],
                    "sourceTableCoordinates": [
                        {
                            "sourceId": "string",
                            "cellRanges": [{"begin": {"column": 0, "row": 0}, "end": {"column": 0, "row": 0}}],
                        }
                    ],
                    "sourceTextCoordinates": [{"sourceId": "string", "charRanges": [{"begin": 0, "end": 0}]}],
                    "coordinates": {},
                    "tableCoordinates": ["string"],
                },
                "aliases": {"additionalProp1": "string", "additionalProp2": "string", "additionalProp3": "string"},
            }
        ],
        "groups": [{"order": 0, "name": "string", "elements": ["string"]}],
    }

    with aioresponses() as mock_response:
        mock_response.put(url, status=HTTPStatus.OK, body=EXTRACTED_DATA_RESPONSE_JSON)

        response = await client.put(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == EXTRACTED_DATA_RESPONSE_DICT


@pytest.mark.asyncio
async def test_save_extracted_data_with_override__ok(client: AsyncClient, document_id: str):
    url = f"{EXTRACTION_BASE_URL}/{document_id}/override"
    data = {
        "fields": [
            {
                "fieldCode": "string",
                "data": {
                    "id": "string",
                    "value": "checked",
                    "confidence": -1,
                    "sourceBboxCoordinates": [{"sourceId": "string", "bboxes": [{"y": 0, "x": 0, "w": 0, "h": 0}]}],
                    "sourceTableCoordinates": [
                        {
                            "sourceId": "string",
                            "cellRanges": [{"begin": {"column": 0, "row": 0}, "end": {"column": 0, "row": 0}}],
                        }
                    ],
                    "sourceTextCoordinates": [{"sourceId": "string", "charRanges": [{"begin": 0, "end": 0}]}],
                    "coordinates": {},
                    "tableCoordinates": ["string"],
                },
                "aliases": {"additionalProp1": "string", "additionalProp2": "string", "additionalProp3": "string"},
            }
        ],
        "groups": [{"order": 0, "name": "string", "elements": ["string"]}],
    }

    with aioresponses() as mock_response:
        mock_response.put(url, status=HTTPStatus.OK, body=EXTRACTED_DATA_RESPONSE_JSON)

        response = await client.put(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data/override",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == EXTRACTED_DATA_RESPONSE_DICT


@pytest.mark.asyncio
async def test_save_partial_extracted_data__ok(client: AsyncClient, document_id: str, field_code: str):
    url = f"{EXTRACTION_BASE_URL}/{document_id}/fields/{field_code}"
    data = {
        "cells": [
            {
                "value": "string",
                "confidence": -1,
                "coordinates": {"column": 0, "row": 0, "colspan": 1, "rowspan": 1},
                "sourceBboxCoordinates": [{"sourceId": "string", "bboxes": [{"y": 0, "x": 0, "w": 0, "h": 0}]}],
                "sourceTableCoordinates": None,
                "sourceTextCoordinates": None,
                "pk": "string",
            }
        ]
    }

    with aioresponses() as mock_response:
        mock_response.patch(url, status=HTTPStatus.OK, body=TABLE_FIELD_CHUNK_RESPONSE_JSON)

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data/{field_code}/table",
            data=json.dumps(data),
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == TABLE_FIELD_CHUNK_RESPONSE_DICT


@pytest.mark.asyncio
async def test_get_table_field_chunk__ok(client: AsyncClient, document_id: str, field_code: str):
    data = {
        "rowsPerChunk": 15,
        "rowsChunk": 5,
        "listIndex": 0,
    }
    url = f"{EXTRACTION_BASE_URL}/{document_id}/fields/{field_code}/chunk?{urlencode(data)}"

    with aioresponses() as mock_response:
        mock_response.get(url, status=HTTPStatus.OK, body=GET_TABLE_FIELD_CHUNK_RESPONSE_JSON)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/extracted-data/{field_code}/table/chunk",
            params=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_TABLE_FIELD_CHUNK_RESPONSE_DICT
