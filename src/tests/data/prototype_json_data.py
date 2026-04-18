import json

from .extraction_json_data import (
    EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT as EF,
)
from .extraction_json_data import (
    EXTRACTION_FIELD_WITH_TABLE_FIELD_TYPE_DICT as TABLE_EF,
)

PROTOTYPE_EF_CREATE_REQUEST_DICT = {
    "name": "string",
    "typeCode": "table",
    "keys": [
        "string",
    ],
    "mappingType": "one_to_one",
    "description": {},
    "required": True,
    "confidential": False,
    "readOnly": False,
}
PROTOTYPE_EF_UPDATE_REQUEST_DICT = {
    "name": "string",
    "description": {},
    "required": True,
    "confidential": True,
    "readOnly": True,
}
PROTOTYPE_MAPPING_CREATE_REQUEST_DICT = {
    "code": "string",
    "typeCode": "table",
    "keys": [
        "string",
    ],
    "mappingType": "one_to_one",
}
PROTOTYPE_MAPPING_UPDATE_REQUEST_DICT = {
    "keys": [
        "string",
    ],
}


PROTOTYPE_MAPPING_RESPONSE_DICT = {
    "code": EF["code"],
    "prototypeId": "string",
    "keys": ["string"],
    "mappingType": "one_to_one",
    "dataType": "string",
}
PROTOTYPE_MAPPING_RESPONSE__JSON = json.dumps(PROTOTYPE_MAPPING_RESPONSE_DICT)

PROTOTYPE_TABULAR_MAPPING_REQUEST_DICT = {
    "code": "test",
    "headerType": "rows",
    "headers": [
        {
            "name": "test",
            "aliases": ["alias1", "alias2"],
        }
    ],
    "occurrenceIndex": 1,
}
PROTOTYPE_TABULAR_MAPPING_RESPONSE_DICT = {
    "code": TABLE_EF["code"],
    "prototypeId": "string",
    "headers": [
        {
            "name": "test",
            "aliases": ["alias1", "alias2"],
        }
    ],
    "headerType": "rows",
    "occurrenceIndex": 1,
}
PROTOTYPE_TABULAR_MAPPING_RESPONSE__JSON = json.dumps(PROTOTYPE_TABULAR_MAPPING_RESPONSE_DICT)

PROTOTYPE_DOCUMENT_TYPE_RESPONSE__DICT = {
    "id": "string",
    "name": "string",
    "engine": "string",
    "language": "string",
    "createdAt": "2024-10-22T05:14:00.035Z",
    "description": "string",
    "mappings": [
        PROTOTYPE_MAPPING_RESPONSE_DICT,
    ],
    "tabularMappings": [
        PROTOTYPE_TABULAR_MAPPING_RESPONSE_DICT,
    ],
}
PROTOTYPE_DOCUMENT_TYPE_RESPONSE__JSON = json.dumps(PROTOTYPE_DOCUMENT_TYPE_RESPONSE__DICT)

PROTOTYPE = PROTOTYPE_DOCUMENT_TYPE_RESPONSE__DICT
MAPPING = PROTOTYPE_MAPPING_RESPONSE_DICT
TABULAR_MAPPING = PROTOTYPE_TABULAR_MAPPING_RESPONSE_DICT

EXPECTED_CONSOLIDATED__FIELD_WITH_MAPPING_DICT = {
    "id": EF["code"],
    "prototypeId": PROTOTYPE["id"],
    "name": EF["name"],
    "fieldType": {
        "typeCode": EF["fieldType"],
        "description": EF["fieldMeta"],
    },
    "mapping": {
        "keys": MAPPING["keys"],
        "mappingType": MAPPING["mappingType"],
        "mappingDataType": MAPPING["dataType"],
    },
    "required": EF["required"],
    "confidential": EF["confidential"],
    "readOnly": EF["readOnly"],
    "order": EF["order"],
}

EXPECTED_CONSOLIDATED_FIELD_WITH_TABULAR_MAPPING_DICT = {
    "id": TABLE_EF["code"],
    "prototypeId": PROTOTYPE["id"],
    "name": TABLE_EF["name"],
    "fieldType": {
        "typeCode": TABLE_EF["fieldType"],
        "description": TABLE_EF["fieldMeta"],
    },
    "tabularMapping": {
        "headers": TABULAR_MAPPING["headers"],
        "headerType": TABULAR_MAPPING["headerType"],
        "occurrenceIndex": TABULAR_MAPPING["occurrenceIndex"],
    },
    "required": TABLE_EF["required"],
    "confidential": TABLE_EF["confidential"],
    "readOnly": TABLE_EF["readOnly"],
    "order": TABLE_EF["order"],
}


EXPECTED_CONSOLIDATED__PROTOTYPE_WITH_EXTRACTION_RESPONSE_DICT = {
    "id": PROTOTYPE["id"],
    "name": PROTOTYPE["name"],
    "engine": PROTOTYPE["engine"],
    "language": PROTOTYPE["language"],
    "createdAt": PROTOTYPE["createdAt"],
    "description": PROTOTYPE["description"],
    "fields": [
        EXPECTED_CONSOLIDATED__FIELD_WITH_MAPPING_DICT,
    ],
    "tableFields": [
        EXPECTED_CONSOLIDATED_FIELD_WITH_TABULAR_MAPPING_DICT,
    ],
}

GET_REFERENCE_LAYOUTS_RESPONSE_DICT = {
    "reference_layouts": [
        {"id": "string", "prototypeId": "string", "title": "string", "state": "New", "blobName": "string"}
    ]
}
GET_REFERENCE_LAYOUTS_RESPONSE_JSON = json.dumps(GET_REFERENCE_LAYOUTS_RESPONSE_DICT)

GET_REFERENCE_LAYOUT_RESPONSE_DICT = {
    "id": "0feb3ab606dc46f48db42002deeaa4b1",
    "prototypeId": "f980df8d414347bb85d350b183a625c8",
    "title": "55130487%20%2847%29%20%281%29_1",
    "state": "Ready",
    "blobName": "ab7d999a0a084f49988b2f418afeadf2.pdf",
}
GET_REFERENCE_LAYOUT_RESPONSE_JSON = json.dumps(GET_REFERENCE_LAYOUT_RESPONSE_DICT)
