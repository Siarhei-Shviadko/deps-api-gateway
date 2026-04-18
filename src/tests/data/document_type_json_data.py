import copy
import datetime as dt
import json

from .workflow_manager_json_data import WORKFLOW_CONFIGURATION_RESPONSE_DICT

DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT = {
    "id": "1",
    "documentType": "new_type_1",
    "tenantId": "deps",
    "fields": [
        {
            "name": "test 1",
            "required": False,
            "order": 0,
            "fieldType": "string",
            "fieldMeta": None,
            "pk": "test 1 code",
            "code": "test_code",
            "documentTypeCode": "e049dce296194a74bb6e8549a9357a41",
            "confidential": False,
            "readOnly": False,
        },
    ],
    "language": "by",
    "engine": "TESSERACT",
    "extractionType": None,
    "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "description": "test description",
    "llmType": "gpt-4",
}
DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON = json.dumps(
    DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT
)
DOCUMENT_TYPE_RESPONSE_FROM_EXTRACTION_SERVICE_DICT = {
    "id": "1",
    "documentType": "new_type_1",
    "tenantId": "deps",
    "extractorType": "plugin",
    "fields": [
        {
            "code": "test 2 code",
            "name": "test 2 name",
            "type": "string",
            "required": True,
            "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
            "promptValue": "test value",
            "confidential": False,
            "readOnly": False,
        },
    ],
}
DOCUMENT_TYPE_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = json.dumps(DOCUMENT_TYPE_RESPONSE_FROM_EXTRACTION_SERVICE_DICT)

DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT_WITHOUT_WORKFLOW_CONFIGURATION = copy.deepcopy(
    DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT
)

DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT = {
    "result": [
        DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT_WITHOUT_WORKFLOW_CONFIGURATION,
        {
            "id": "2",
            "documentType": "new_type_2",
            "tenantId": "deps",
            "fields": [
                {
                    "name": "string1",
                    "required": False,
                    "order": 0,
                    "fieldType": "string",
                    "fieldMeta": None,
                    "pk": "string1",
                    "code": "string1",
                    "documentTypeCode": "b32795a38fb74102b8d38b6800b61e29",
                    "confidential": False,
                    "readOnly": False,
                },
            ],
            "extractionType": None,
            "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
            "description": "test description",
            "llmType": "gpt-4",
        },
    ],
}

DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON = json.dumps(
    DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT
)

DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT_WITH_WORKFLOW_CONFIGURATION = copy.deepcopy(
    DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT
)
for doctype in DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT_WITH_WORKFLOW_CONFIGURATION["result"]:
    doctype["workflowConfiguration"] = WORKFLOW_CONFIGURATION_RESPONSE_DICT  # type: ignore

DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_WITH_WORKFLOW_CONFIGURATION_SERVICE_JSON = json.dumps(
    DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT_WITH_WORKFLOW_CONFIGURATION
)

DOCUMENT_TYPES_RESPONSE_FROM_EXTRACTION_SERVICE_DICT = {
    "result": [copy.deepcopy(DOCUMENT_TYPE_RESPONSE_FROM_EXTRACTION_SERVICE_DICT)],
}
DOCUMENT_TYPES_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = json.dumps(DOCUMENT_TYPES_RESPONSE_FROM_EXTRACTION_SERVICE_DICT)

DOCUMENT_TYPES_ATTACH_PLUGIN_EXTRACTOR_REQUEST = {
    "documentType": "documentType11",
    "plugin": {
        "name": "test t111",
        "engine": "TESSERACT",
        "language": "eng",
        "imageTransformations": [
            "test transformation",
        ],
        "fields": [
            {
                "name": "string",
                "required": False,
                "readOnly": False,
                "confidential": False,
                "order": 1,
                "fieldType": "string",
                "fieldMeta": {},
                "promptValue": "string1",
                "pk": "string1",
                "code": "string1",
            },
        ],
        "description": "test 11 description",
    },
}

DOCUMENT_TYPES_ATTACH_EXTRACTOR_REQUEST = {
    "name": "test t111",
    "extractorType": "plugin",
    "engine": "TESSERACT",
    "language": "eng",
    "imageTransformations": ["test transformation"],
    "fields": [
        {
            "name": "string",
            "required": False,
            "readOnly": False,
            "confidential": False,
            "order": 1,
            "fieldType": "string",
            "fieldMeta": {},
            "promptValue": "string1",
            "pk": "string1",
            "code": "string1",
        },
    ],
    "description": "test 11 description",
}

DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE = {
    "command_channel": "documentType11-test_tenant",
    "documentTypeId": "bb090f9d6db649659a3f105604b28a9d",
}

CREATE_TEMPLATE_RESPONSE_DICT = {"templateId": "string"}
CREATE_TEMPLATE_RESPONSE_JSON = json.dumps(CREATE_TEMPLATE_RESPONSE_DICT)

GET_TEMPLATE_VERSIONS_RESPONSE_LIST = [
    {"id": "string", "name": "string", "createdAt": "2024-10-29T16:04:31.492585", "description": "string"}
]
GET_TEMPLATE_VERSIONS_RESPONSE_JSON = json.dumps(GET_TEMPLATE_VERSIONS_RESPONSE_LIST)
GET_TEMPLATE_VERSIONS_RESPONSE_DICT = {"versions": GET_TEMPLATE_VERSIONS_RESPONSE_LIST}

SERIALIZED_TEMPLATE_VERSION_RESPONSE_DICT = {
    "id": "string",
    "name": "string",
    "createdAt": "2024-12-04T10:49:42.076Z",
    "templateId": "string",
    "originalFiles": ["string"],
    "referencePages": [
        {
            "id": "string",
            "blobName": "string",
            "markups": [{"code": "string", "type": "string", "coordinates": [{"x": 1, "y": 1, "w": 1, "h": 1}]}],
        }
    ],
    "description": "string",
}
SERIALIZED_TEMPLATE_VERSION_RESPONSE_JSON = json.dumps(SERIALIZED_TEMPLATE_VERSION_RESPONSE_DICT)
