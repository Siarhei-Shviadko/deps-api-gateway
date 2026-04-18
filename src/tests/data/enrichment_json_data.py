import json

CREATE_EXTRA_FIELD_RESPONSE_DICT = {"code": "f5655af41fe34246b0c2d1f2ae060514"}
CREATE_EXTRA_FIELD_RESPONSE_JSON = json.dumps(CREATE_EXTRA_FIELD_RESPONSE_DICT)


SUPPLEMENT_DATA_CREATE_OR_PUT_DICT = {
    "data": [
        {
            "name": "Norma Fisher 1",
            "value": "test value 1",
            "code": "test code 1",
        },
        {
            "name": "Norma Fisher 2",
            "value": "test value 1",
        },
    ],
}
SUPPLEMENT_DATA_CREATE_OR_PUT_JSON = json.dumps(SUPPLEMENT_DATA_CREATE_OR_PUT_DICT)
SUPPLEMENT_DATA_DICT = {
    "data": [
        {
            "code": "21e28fc4134d496c81d4251f3be3ea9c",
            "name": "Norma Fisher 1",
            "type": "string",
            "value": "test value 1",
        },
        {
            "code": "74e28fc4134d495c81d4251f3be3ea6a",
            "name": "Norma Fisher 2",
            "type": "string",
            "value": "test value 1",
        },
    ],
}

SUPPLEMENT_DATA_JSON = json.dumps(SUPPLEMENT_DATA_DICT)
CREATE_OR_MODIFY_SUPPLEMENT_ENTITY_DICT = {"entityId": "test_entity_id"}
CREATE_OR_MODIFY_SUPPLEMENT_ENTITY_JSON = json.dumps(CREATE_OR_MODIFY_SUPPLEMENT_ENTITY_DICT)

SUPPLEMENT_NOT_FOUND_RESPONSE_DICT = {"code": "supplement_not_found_error", "message": "Supplement not found"}
SUPPLEMENT_NOT_FOUND_RESPONSE_JSON = json.dumps(SUPPLEMENT_NOT_FOUND_RESPONSE_DICT)

EXTRA_FIELDS_RESPONSE_DICT = {
    "fields": [{"code": "extra field 1", "name": "extra field 1", "type": "string", "autoFilled": False, "order": 0}]
}
EXTRA_FIELDS_RESPONSE_JSON = json.dumps(EXTRA_FIELDS_RESPONSE_DICT)
