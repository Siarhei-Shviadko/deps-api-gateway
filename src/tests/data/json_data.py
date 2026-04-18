import datetime as dt
import json
import uuid

RESPONSE_FORM_PREPROCESS_JSON = {
    "documentId": 27632,
    "elements": [
        {
            "id": "ce00bee6d5304bc1929b97c41efc7992",
            "page": 1,
            "blobName": "631e11c060504e6b8a242cd451a3c2cc/preview/0.png",
            "width": 2000,
            "height": 2827,
            "appliedTransformation": None,
            "originalImageId": None,
        }
    ],
}

RESPONSE_FROM_PREPROCESS_RAW = json.dumps(RESPONSE_FORM_PREPROCESS_JSON)

RESPONSE_FORM_UNIFIER_JSON = {
    "documentId": 27632,
    "elements": [
        {
            "id": "ce00bee6d5344bc1929b97c41efc7992",
            "page": 1,
            "blobName": "631e11c360504e6b8a242cd451a3c2cc/preview/123.png",
            "width": 2010,
            "height": 2827,
            "appliedTransformation": None,
            "originalImageId": None,
        }
    ],
}

RESPONSE_FORM_UNIFIER_RAW = json.dumps(RESPONSE_FORM_UNIFIER_JSON)

RESPONSE_FORM_PREPROCESS_TABLE_CELLS_JSON = [
    {
        "value": {"content": "THE ONLY ONE THING THEY FEAR IS YOU", "confidence": 1.0},
        "coordinates": {"column": 0, "row": 0, "colspan": 1, "rowspan": 1},
    }
]

RESPONSE_FORM_PREPROCESS_TABLE_CELLS_RAW = json.dumps(RESPONSE_FORM_PREPROCESS_TABLE_CELLS_JSON)

RESPONSE_FORM_UNIFIER_TABLE_CELLS_JSON = [
    {
        "value": {"content": "THE ONLY ONE THING THEY LOVE IS YOU", "confidence": 1.0},
        "coordinates": {"column": 0, "row": 0, "colspan": 1, "rowspan": 1},
    }
]

RESPONSE_FORM_UNIFIER_TABLE_CELLS_RAW = json.dumps(RESPONSE_FORM_UNIFIER_TABLE_CELLS_JSON)

RESPONSE_FROM_DOCUMENT_SERVICE_RAW = """
{
    "meta": {"total": 3, "size": 1},
    "result": [
        {
            "_id": "82",
            "parentId": null,
            "title": "4506-C searchable-1",
            "state": "dataExtraction",
            "files": null,
            "documentType": "1",
            "modelName": null,
            "date": "2023-01-27",
            "source": null,
            "reviewer": null,
            "labels": [],
            "language": "eng",
            "engine": "TESSERACT",
            "communication": null,
            "previewDocuments": null,
            "processingDocuments": null,
            "error": null,
            "containerType": null,
            "containerMetadata": null,
            "assignedRelations": [],
            "assignmentStatus": "unassigned",
            "priority": "low"
}
]
}
"""
TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW = """
{
    "meta": {"total": 1, "size": 1},
    "result": [
        {
            "pk": 1320,
            "code": "111",
            "name": "111",
            "engine": "TESSERACT",
            "language": "eng",
            "fields": [],
            "extractionType": "ml",
            "inProgress": true,
            "created_at": "2023-09-20T10:45:06.971076+00:00",
            "description": "test description",
            "llmType": "gpt-4"
        }
    ]
}
"""
UPLOAD_DOCUMENT_RESPONSE_RAW = """
{
    "id": "83",
    "message": "Very successful"
}
"""

RESPONSE_FROM_DOCUMENT_SERVICE_JSON = json.loads(RESPONSE_FROM_DOCUMENT_SERVICE_RAW)
UPLOAD_DOCUMENT_RESPONSE_JSON = json.loads(UPLOAD_DOCUMENT_RESPONSE_RAW)
TYPES_RESPONSE_FROM_CORLEONE_SERVICE_JSON = json.loads(TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW)

TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON = [
    {
        "id": uuid.uuid4().hex,
        "documentType": "new_type_1",
        "tenantId": "deps",
        "fields": [],
        "language": "by",
        "engine": "TESSERACT",
        "extractionType": None,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "description": "test description",
        "llmType": "gpt-4",
    },
    {
        "id": "1",
        "documentType": "new_type_2",
        "tenantId": "deps",
        "fields": [],
        "extractionType": None,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "description": "test description",
        "llmType": "gpt-4",
    },
]
TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW = json.dumps(TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON)


TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON = {
    "id": uuid.uuid4().hex,
    "documentType": "new_type_1",
    "tenantId": "deps",
    "extractionType": "plugin",
    "fields": [],
    "language": "by",
    "engine": "TESSERACT",
    "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "description": "test description",
    "llmType": "gpt-4",
}

TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON = {
    "pk": 1320,
    "code": "111",
    "name": "111",
    "engine": "TESSERACT",
    "language": "eng",
    "fields": [],
    "extractionType": "ml",
    "inProgress": True,
    "createdAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "description": "test description corleone",
}

TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW = json.dumps(TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON)
TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW = json.dumps(TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON)
CREATE_DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON = {
    "documentTypeId": uuid.uuid4().hex,
}
CREATE_DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW = json.dumps(
    CREATE_DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON
)
CREATE_DOCUMENT_TYPE_REQUEST = json.dumps({"name": "test name", "description": "test description"})

EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON = [
    {
        "fieldPk": 2449,
        "data": [
            {
                "key": {
                    "value": "",
                    "sourceId": None,
                    "coordinates": None,
                    "tableCoordinates": [],
                    "confidence": None,
                    "sourceBboxCoordinates": None,
                    "sourceTableCoordinates": None,
                    "sourceTextCoordinates": None,
                    "setIndex": None,
                },
                "value": {
                    "value": "Test field",
                    "sourceId": None,
                    "coordinates": {
                        "y": 0.054225250988998386,
                        "x": 0.7009432373046875,
                        "w": 0.22249999999999992,
                        "h": 0.015917934205871953,
                        "page": 1,
                    },
                    "tableCoordinates": [],
                    "confidence": 0.9755755066871643,
                    "sourceBboxCoordinates": None,
                    "sourceTableCoordinates": None,
                    "sourceTextCoordinates": None,
                    "setIndex": None,
                },
            }
        ],
        "isInGoldenData": False,
    },
]

EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = [
    {
        "fieldCode": "buyerName",
        "data": [
            {
                "key": {
                    "value": "",
                    "confidence": 1,
                    "sourceBboxCoordinates": None,
                    "sourceTableCoordinates": None,
                    "sourceTextCoordinates": None,
                },
                "value": {
                    "value": "EPAM SYSTEMS",
                    "confidence": 0.9131583571434021,
                    "sourceBboxCoordinates": [
                        {
                            "sourceId": "75aa0a9df07c41a5bcbab14751417f48",
                            "bboxes": [
                                {
                                    "y": 0.15901966372185808,
                                    "x": 0.06330645161290323,
                                    "w": 0.16774193548387095,
                                    "h": 0.009119407238529498,
                                }
                            ],
                        }
                    ],
                    "sourceTableCoordinates": None,
                    "sourceTextCoordinates": None,
                },
            }
        ],
    },
]

# RUN_PIPELINE_
document_for_old_pipeline = {
    "_id": 1,
    "title": "doc_type_from_corleone",
    "documentType": TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON["code"],
}

document_for_workflow_pipeline = {
    "_id": 2,
    "title": "doc_type_from_document_type",
    "documentType": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"],
}

DOCUMENT_DETAIL_RESPONSE_1_JSON = json.dumps(document_for_old_pipeline)
DOCUMENT_DETAIL_RESPONSE_2_JSON = json.dumps(document_for_workflow_pipeline)
EDATA_RESPONSE_FROM_CORLEONE_SERVICE_RAW = json.dumps(EDATA_RESPONSE_FROM_CORLEONE_SERVICE_JSON)
EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_RAW = json.dumps(EDATA_RESPONSE_FROM_EXTRACTION_SERVICE_JSON)

DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_JSON = {"deletedFieldPks": [111]}
DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = {"message": "Successfully deleted."}

DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_RAW = json.dumps(
    DELETE_EDATA_FIELDS_RESPONSE_FROM_CORLEONE_SERVICE_JSON
)
DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW = json.dumps(
    DELETE_EDATA_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON
)

CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_JSON = {
    "data": "corleone",
}

CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_RAW = json.dumps(CHUNK_RESPONSE_FROM_CORLEONE_SERVICE_JSON)

CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = {
    "data": "extraction",
}

CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_RAW = json.dumps(CHUNK_RESPONSE_FROM_EXTRACTION_SERVICE_JSON)

EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON = {"data": "corleone"}
EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON = {"data": "extraction"}

EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_RAW = json.dumps(EDATA_CELLS_RESPONSE_FROM_CORLEONE_SERVICE_JSON)
EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_RAW = json.dumps(EDATA_CELLS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON)

OCR_ENGINES_RESPONSE = [
    {"code": "TESSERACT", "name": "Tesseract"},
    {"code": "CRAFT_TESSERACT", "name": "Craft + Tesseract"},
    {"code": "EASYOCR", "name": "EasyOCR"},
    {"code": "PADDLEOCR", "name": "PaddleOCR"},
]
RAW_OCR_ENGINES_RESPONSE = json.dumps(OCR_ENGINES_RESPONSE)

OCR_LANGUAGES_RESPONSE = [
    {"code": "eng", "name": "English"},
    {"code": "rus", "name": "Russian"},
    {"code": "chi_sim", "name": "Simplified Chinese"},
    {"code": "deu", "name": "German"},
    {"code": "spa", "name": "Spanish"},
    {"code": "ukr", "name": "Ukrainian"},
]
RAW_OCR_LANGUAGES_RESPONSE = json.dumps(OCR_LANGUAGES_RESPONSE)

DOCUMENT_STATES_RESPONSE = {
    "preprocessing": {"title": "Preprocessing", "name": "preprocessing"},
    "identification": {"title": "Identification", "name": "identification"},
    "new": {"title": "New", "name": "new"},
    "inReview": {"title": "In Review", "name": "inReview"},
    "failed": {"title": "Failed", "name": "failed"},
    "completed": {"title": "Completed", "name": "completed"},
    "dataExtraction": {"title": "Data Extraction", "name": "dataExtraction"},
    "validation": {"title": "Validation", "name": "validation"},
    "closed": {"title": "Closed", "name": "closed"},
}
RAW_DOCUMENT_STATES_RESPONSE = json.dumps(DOCUMENT_STATES_RESPONSE)


UPDATE_DOCUMENT_TYPE_LLM_RAW_REQUEST = json.dumps(
    {
        "llmType": "gpt-4",
    }
)
