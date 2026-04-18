import datetime as dt
import json

TEMPLATE_FIELD = {
    "pk": "test code",
    "code": "test code",
    "name": "new name",
    "fieldType": "string",
    "required": True,
    "fieldMeta": {},
    "confidential": True,
    "readOnly": True,
    "promptValue": None,
    "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "order": 0,
}

TEMPLATE_FIELD_CREATE_REQUEST_DICT = {
    "code": "test code 1",
    "name": "name 1",
    "type": "string",
    "description": {},
    "required": True,
    "readOnly": False,
    "confidential": False,
}

TEMPLATE_FIELD_UPDATE_REQUEST_DICT = {
    "name": "name 2",
    "description": {},
    "required": True,
    "readOnly": False,
    "confidential": False,
}

TEMPLATE_FIELDS_RESPONSE_LIST = [
    {
        "id": TEMPLATE_FIELD["code"],
        "name": TEMPLATE_FIELD["name"],
        "code": TEMPLATE_FIELD["code"],
        "type": TEMPLATE_FIELD["fieldType"],
        "description": TEMPLATE_FIELD["fieldMeta"],
        "required": TEMPLATE_FIELD["required"],
        "readOnly": TEMPLATE_FIELD["readOnly"],
        "confidential": TEMPLATE_FIELD["confidential"],
        "order": TEMPLATE_FIELD["order"],
        "promptValue": TEMPLATE_FIELD["promptValue"],
        "createdAt": TEMPLATE_FIELD["createdAt"],
    }
]

DOCUMENT_TYPE_WITH_TEMPLATE_FIELDS_RESPONSE_DICT = {
    "id": "1",
    "documentType": "new_type_1",
    "tenantId": "deps",
    "fields": [
        TEMPLATE_FIELD,
    ],
    "language": "by",
    "engine": "TESSERACT",
    "extractionType": None,
    "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "description": "test description",
}
DOCUMENT_TYPE_WITH_TEMPLATE_FIELDS_RESPONSE_JSON = json.dumps(DOCUMENT_TYPE_WITH_TEMPLATE_FIELDS_RESPONSE_DICT)
