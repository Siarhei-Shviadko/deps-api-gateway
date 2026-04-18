import json
import random
import uuid

HIGH_SPARROW_VALIDATION_RESULTS_NOT_VALID_DICT = {
    "isValid": False,
    "detail": [
        {
            "fieldCode": "TestField",
            "documentId": uuid.uuid4().hex,
            "errors": [
                {
                    "severity": "error",
                    "type": "rules_check",
                    "message": "error message",
                    "column": 0,
                    "row": 0,
                    "index": 0,
                    "kvId": "TestkvId1",
                }
            ],
            "warnings": [
                {
                    "severity": "warning",
                    "type": "pre_check",
                    "message": "warning message",
                    "column": 1,
                    "row": 1,
                    "index": 1,
                    "kvId": "TestkvId2",
                }
            ],
        }
    ],
}
HIGH_SPARROW_VALIDATION_RESULTS_NOT_VALID_JSON = json.dumps(HIGH_SPARROW_VALIDATION_RESULTS_NOT_VALID_DICT)

HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT = {
    "isValid": True,
    "detail": [
        {
            "fieldCode": "TestField",
            "documentId": uuid.uuid4().hex,
            "errors": [
                {
                    "severity": "error",
                    "type": "rules_check",
                    "message": "error message",
                    "column": None,
                    "row": None,
                    "index": None,
                    "kvId": None,
                }
            ],
            "warnings": [
                {
                    "severity": "warning",
                    "type": "pre_check",
                    "message": "warning message",
                    "column": 1,
                    "row": 1,
                    "index": 1,
                    "kvId": "kvId",
                }
            ],
        }
    ],
}
HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON = json.dumps(HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT)

HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_DICT = {
    "code": "validation_result_not_found",
    "message": f"Validation result with id: `{uuid.uuid4().hex}` not found",
}
HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_JSON = json.dumps(HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_DICT)

VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_DICT = {
    "detail": [
        {
            "documentId": random.randint(1, 10000),
            "errors": [{"column": 1, "index": 1, "message": uuid.uuid4().hex, "row": 1}],
            "fieldCode": uuid.uuid4().hex,
            "warnings": [{"column": None, "index": None, "message": uuid.uuid4().hex, "row": None}],
        }
    ],
    "isValid": False,
}
VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_JSON = json.dumps(VALIDATION_SERVICE_VALIDATION_RESULTS_VALID_DICT)

VALIDATION_SERVICE_VALIDATION_RESULTS_NOT_FOUND_DICT = {
    "code": "validation_results_not_found",
    "message": f"No validation results for document pk: {random.randint(1, 10000)}",
}
VALIDATION_SERVICE_VALIDATION_RESULTS_NOT_FOUND_JSON = json.dumps(VALIDATION_SERVICE_VALIDATION_RESULTS_NOT_FOUND_DICT)

HIGH_SPARROW_CREATE_RULE_DICT = {
    "name": uuid.uuid4().hex,
    "severity": "error",
    "rule": uuid.uuid4().hex,
    "issue_message": uuid.uuid4().hex,
    "description": uuid.uuid4().hex,
    "need_warning_even_if_optional": False,
    "for_each": False,
    "for_any": False,
    "check_optional_fields": False,
}
HIGH_SPARROW_CREATE_RULE_JSON = json.dumps(HIGH_SPARROW_CREATE_RULE_DICT)

HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_DICT = {
    "id": "c04b2c16ec6b4551ab137953470a555f",
    "tenantId": "8c5457a8a6ea41c0af5112f9d897a5f5",
    "validators": [
        {
            "code": "8c5457a8a6ea41c0af5112f9d897a5f5",
            "type": {"type": "string", "description": {"maxLength": 1000}},
            "isRequired": True,
            "rules": [],
        },
    ],
    "externalValidators": [],
    "crossFieldValidators": [],
}
HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_JSON = json.dumps(HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_DICT)

GET_ALL_VALIDATORS_RESPONSE_DICT = {
    "validators": [
        {
            "code": "8c5457a8a6ea41c0af5112f9d897a5f5",
            "type": {"type": "string", "description": {"maxLength": 1000}},
            "isRequired": True,
            "rules": [],
        },
    ],
    "externalValidators": [
        {"name": "name", "url": "http://test.site/validate"},
    ],
    "crossFieldValidators": [
        {
            "id": uuid.uuid4().hex,
            "name": "name",
            "description": "",
            "rule": "rule",
            "severity": "error",
            "validated_fields": [uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex],
            "issue_message": {
                "message": "message",
                "dependent_fields": [uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex],
            },
            "for_each": False,
            "for_any": True,
        },
    ],
}
GET_ALL_VALIDATORS_RESPONSE_JSON = json.dumps(GET_ALL_VALIDATORS_RESPONSE_DICT)

HIGH_SPARROW_VALIDATE_FIELD_OK_DICT = {
    "isValid": True,
    "detail": [],
}
HIGH_SPARROW_VALIDATE_FIELD_OK_JSON = json.dumps(HIGH_SPARROW_VALIDATE_FIELD_OK_DICT)

HIGH_SPARROW_VALIDATE_FIELD_NOT_VALID_DICT = {
    "isValid": False,
    "detail": [
        {
            "fieldCode": "TestField",
            "documentId": uuid.uuid4().hex,
            "errors": [
                {
                    "severity": "error",
                    "type": "rules_check",
                    "message": "field value is invalid",
                    "column": 0,
                    "row": 0,
                    "index": 0,
                    "kvId": None,
                }
            ],
            "warnings": [],
        }
    ],
}
HIGH_SPARROW_VALIDATE_FIELD_NOT_VALID_JSON = json.dumps(HIGH_SPARROW_VALIDATE_FIELD_NOT_VALID_DICT)

HIGH_SPARROW_VALIDATE_FIELD_NOT_FOUND_DICT = {
    "code": "document_type_not_found",
    "message": f"Document type with id: `{uuid.uuid4().hex}` not found",
}
HIGH_SPARROW_VALIDATE_FIELD_NOT_FOUND_JSON = json.dumps(HIGH_SPARROW_VALIDATE_FIELD_NOT_FOUND_DICT)
