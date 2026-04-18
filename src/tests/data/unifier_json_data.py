import json
import uuid

UNIFIED_DATA_DICT = {
    "documentId": uuid.uuid4().hex,
    "elements": [
        {
            "id": uuid.uuid4().hex,
            "page": 0,
            "blobName": uuid.uuid4().hex,
            "width": 0,
            "height": 0,
            "appliedTransformation": {"name": "test_name", "parameters": {"args": [], "kwargs": {}}},
            "originalImageId": uuid.uuid4().hex,
        },
        {
            "id": uuid.uuid4().hex,
            "imageId": uuid.uuid4().hex,
            "page": 1,
            "wordboxes": [{"word": {"content": "test", "confidence": 1}, "bbox": {"x": 1, "y": 1, "w": 1, "h": 1}}],
        },
        {
            "id": uuid.uuid4().hex,
            "page": 2,
            "maxColumn": 2,
            "maxRow": 2,
            "coordinates": {"x": 2, "y": 2, "w": 2, "h": 2},
            "name": "test_name",
        },
    ],
}
UNIFIED_DATA_JSON = json.dumps(UNIFIED_DATA_DICT)

UNIFIED_DATA_NOT_FOUND_DICT = {
    "code": "unified_data_not_found_error",
    "message": f"Unified data with {uuid.uuid4().hex} document id not found",
}
UNIFIED_DATA_NOT_FOUND_JSON = json.dumps(UNIFIED_DATA_NOT_FOUND_DICT)

UNIFIED_CELLS_DATA_DICT = [
    {
        "value": {
            "content": "test",
            "confidence": 1.0,
        },
        "coordinates": {
            "column": 0,
            "row": 0,
            "colspan": 1,
            "rowspan": 1,
        },
        "table_id": uuid.uuid4().hex,
    },
    {
        "value": None,
        "coordinates": {
            "column": 1,
            "row": 0,
            "colspan": 1,
            "rowspan": 1,
        },
        "table_id": uuid.uuid4().hex,
    },
    {
        "value": {
            "content": "test2",
            "confidence": 0.9,
        },
        "coordinates": {
            "column": 0,
            "row": 1,
            "colspan": 1,
            "rowspan": 1,
        },
        "table_id": uuid.uuid4().hex,
    },
]
UNIFIED_CELLS_DATA_JSON = json.dumps(UNIFIED_CELLS_DATA_DICT)
