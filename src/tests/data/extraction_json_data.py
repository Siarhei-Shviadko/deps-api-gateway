import datetime as dt
import json
import uuid

EXTRACTION_FIELD_WITH_PROMPT_REQUEST_DICT = {
    "name": "new name",
    "promptValue": "new prompt",
    "required": True,
}

EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT = {
    "pk": "test code",
    "code": "test code",
    "name": "new name",
    "fieldType": "string",
    "required": True,
    "fieldMeta": {},
    "promptValue": "new prompt",
    "confidential": True,
    "readOnly": True,
    "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "order": 0,
}

EXTRACTION_FIELD_WITH_TABLE_FIELD_TYPE_DICT = {
    "pk": "test code 2",
    "code": "test code 2",
    "name": "table name",
    "fieldType": "table",
    "required": True,
    "fieldMeta": {},
    "promptValue": "new prompt",
    "confidential": True,
    "readOnly": True,
    "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "order": 1,
}
EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = json.dumps(
    EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT
)
EXTRACTION_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = json.dumps(
    {"fields": [EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON]},
)

EXTRACTION_DOCUMENT_TYPE_RESPONSE_DICT = {
    "id": "1",
    "documentType": "new_type_1",
    "tenantId": "deps",
    "fields": [
        EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT,
        EXTRACTION_FIELD_WITH_TABLE_FIELD_TYPE_DICT,
    ],
    "language": "by",
    "engine": "TESSERACT",
    "extractionType": None,
    "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "description": "test description",
    "llmExtractionParams": {
        "customInstruction": uuid.uuid4().hex,
        "groupingFactor": 10,
        "temperature": 0.333,
    },
}
EXTRACTION_DOCUMENT_TYPE_RESPONSE__JSON = json.dumps(EXTRACTION_DOCUMENT_TYPE_RESPONSE_DICT)

EXTRACTED_DATA_RESPONSE_DICT = {
    "documentId": 0,
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
        }
    ],
    "groups": [{"order": 0, "name": "string", "elements": ["string"]}],
}
EXTRACTED_DATA_RESPONSE_JSON = json.dumps(EXTRACTED_DATA_RESPONSE_DICT)

TABLE_FIELD_CHUNK_RESPONSE_DICT = {
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
TABLE_FIELD_CHUNK_RESPONSE_JSON = json.dumps(TABLE_FIELD_CHUNK_RESPONSE_DICT)

GET_TABLE_FIELD_CHUNK_RESPONSE_DICT = {
    "meta": {"rowsChunk": 5, "chunksTotal": 55, "rowsTotal": 55, "listIndex": 0},
    "data": {
        "cells": [
            {
                "pk": "string",
                "value": "string",
                "confidence": -1,
                "coordinates": {"column": 0, "row": 0, "colspan": 1, "rowspan": 1},
                "sourceBboxCoordinates": [{"sourceId": "string", "bboxes": [{"y": 0, "x": 0, "w": 0, "h": 0}]}],
                "sourceTableCoordinates": None,
                "sourceTextCoordinates": None,
            }
        ]
    },
}
GET_TABLE_FIELD_CHUNK_RESPONSE_JSON = json.dumps(GET_TABLE_FIELD_CHUNK_RESPONSE_DICT)

UPDATE_EXTRACTION_FIELD_RESPONSE_DICT = {
    "name": "string",
    "code": "string",
    "pk": "string",
    "documentTypeCode": "string",
    "required": False,
    "order": 0,
    "fieldType": "string",
    "confidential": False,
    "readOnly": False,
    "fieldMeta": {},
}
UPDATE_EXTRACTION_FIELD_RESPONSE_JSON = json.dumps(UPDATE_EXTRACTION_FIELD_RESPONSE_DICT)
