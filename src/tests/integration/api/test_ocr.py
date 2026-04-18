import json
import uuid
from http import HTTPStatus
from unittest.mock import mock_open, patch

import pytest
from aioresponses import aioresponses

from deps_api_gateway.application.tools import OCREngineEnum
from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    OCR_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from tests.data.ocr_json_data import (
    EXTRACT_AREA_DATA_DICT,
    EXTRACT_AREA_DATA_JSON,
    EXTRACT_IMAGE_PAGE_DATA_DICT,
    EXTRACT_IMAGE_PAGE_DATA_JSON,
    EXTRACT_TEXT_DATA_DICT,
    EXTRACT_TEXT_DATA_JSON,
    LANGUAGES_DATA_DICT,
    LANGUAGES_DATA_JSON,
    OCR_ENGINES_DATA_DICT,
    OCR_ENGINES_DATA_JSON,
)

OCR_V1_BASE_URL = f"{OCR_BASE_API_PREFIX}{V1_PREFIX}"
OCR_V2_BASE_URL = f"{OCR_BASE_API_PREFIX}{V2_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.ocr
async def test_get_languages__ok(client):
    ocr_url = f"{OCR_V1_BASE_URL}/languages"
    with aioresponses() as mock_response:
        mock_response.get(ocr_url, body=LANGUAGES_DATA_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/tools/ocr/languages")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == LANGUAGES_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.ocr
async def test_get_engines__ok(client):
    ocr_url = f"{OCR_V2_BASE_URL}/engines"
    with aioresponses() as mock_response:
        mock_response.get(ocr_url, body=OCR_ENGINES_DATA_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/tools/ocr/engines")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == OCR_ENGINES_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.ocr
async def test_extract_area__ok(client):
    ocr_url = f"{OCR_V2_BASE_URL}/extract-area"
    with aioresponses() as mock_response:
        mock_response.post(ocr_url, body=EXTRACT_AREA_DATA_JSON)

        data = {
            "engine": OCREngineEnum.TESSERACT.value,
            "blobFile": uuid.uuid4().hex,
            "forceOCR": False,
            "language": "eng",
            "area": {"x": 0, "y": 0, "w": 1, "h": 1},
            "engineSettings": "{}",
        }

        response = await client.post(f"{BASE_API_V5_PREFIX}/tools/ocr/extract-area", data=json.dumps(data))

        assert response.status_code == HTTPStatus.OK
        assert response.json() == EXTRACT_AREA_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.ocr
async def test_extract_text__ok(client):
    ocr_url = f"{OCR_V2_BASE_URL}/extract-text"
    with aioresponses() as mock_response:
        mock_response.post(ocr_url, body=EXTRACT_TEXT_DATA_JSON)

        with patch("builtins.open", mock_open(read_data="file")) as mock_file:
            file = open(mock_file, "rb")
        with patch("builtins.open", mock_open(read_data="metadata")) as mock_metadata:
            metadata = open(mock_metadata, "rb")

        data = {
            "engine": OCREngineEnum.TESSERACT.value,
            "language": "eng",
            "engineSettings": "{}",
        }
        files = {"file": (uuid.uuid4().hex, file), "metadata": (uuid.uuid4().hex, metadata)}

        response = await client.post(f"{BASE_API_V5_PREFIX}/tools/ocr/extract-text", files=files, data=data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == EXTRACT_TEXT_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.ocr
async def test_extract_image_page__ok(client):
    ocr_url = f"{OCR_V2_BASE_URL}/extract-image-page"
    with aioresponses() as mock_response:
        mock_response.post(ocr_url, body=EXTRACT_IMAGE_PAGE_DATA_JSON)

        data = {
            "blobName": uuid.uuid4().hex,
            "engine": OCREngineEnum.TESSERACT.value,
            "language": "eng",
        }

        response = await client.post(f"{BASE_API_V5_PREFIX}/tools/ocr/extract-image-page", data=json.dumps(data))

        assert response.status_code == HTTPStatus.OK
        assert response.json() == EXTRACT_IMAGE_PAGE_DATA_DICT
