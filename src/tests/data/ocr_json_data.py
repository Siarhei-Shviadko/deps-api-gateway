import json
import uuid

from deps_api_gateway.application.tools import OCREngineEnum

LANGUAGES_LIST = [{"code": "eng", "name": "English"}]
LANGUAGES_DATA_DICT = {"languages": LANGUAGES_LIST}
LANGUAGES_DATA_JSON = json.dumps(LANGUAGES_LIST)

OCR_ENGINES_LIST = [{"code": OCREngineEnum.TESSERACT.value, "name": "Tesseract"}]
OCR_ENGINES_DATA_DICT = {"engines": OCR_ENGINES_LIST}
OCR_ENGINES_DATA_JSON = json.dumps(OCR_ENGINES_LIST)

EXTRACT_AREA_DATA_DICT = {"content": uuid.uuid4().hex, "bbox": {"x": 0, "y": 0, "w": 1, "h": 1}, "confidence": 0.5}
EXTRACT_AREA_DATA_JSON = json.dumps(EXTRACT_AREA_DATA_DICT)

TEXT_LINES_LIST = [
    {
        "id": 0,
        "wordBoxes": [{"content": uuid.uuid4().hex, "bbox": {"x": 0, "y": 0, "w": 1, "h": 1}, "confidence": 0.5}],
    }
]
EXTRACT_TEXT_DATA_DICT = {"textLines": TEXT_LINES_LIST}
EXTRACT_TEXT_DATA_JSON = json.dumps(TEXT_LINES_LIST)

EXTRACT_IMAGE_PAGE_DATA_DICT = {
    "textLines": [
        {
            "id": 0,
            "wordBoxes": [{"content": uuid.uuid4().hex, "bbox": {"x": 0, "y": 0, "w": 1, "h": 1}, "confidence": 0.5}],
        }
    ]
}
EXTRACT_IMAGE_PAGE_DATA_JSON = json.dumps(EXTRACT_IMAGE_PAGE_DATA_DICT)
