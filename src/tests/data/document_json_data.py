import copy
import json

PARTIAL_UPDATE_DOCUMENT_RESPONSE_DICT = {"_id": "1"}
PARTIAL_UPDATE_DOCUMENT_RESPONSE_JSON = json.dumps(PARTIAL_UPDATE_DOCUMENT_RESPONSE_DICT)

DELETE_DOCUMENT_LIST_RESPONSE_JSON = json.dumps({"deletedDocumentKeys": [{"_id": "1"}, {"_id": "2"}]})

ADD_COMMENT_RESPONSE_DICT = {"text": "string", "createdAt": "2024-11-26T15:54:56.328Z", "createdBy": "string"}
ADD_COMMENT_RESPONSE_JSON = json.dumps(ADD_COMMENT_RESPONSE_DICT)

GET_LABELS_RESPONSE_LIST = [{"_id": "string", "name": "string"}]
GET_LABELS_RESPONSE_JSON = json.dumps(GET_LABELS_RESPONSE_LIST)
GET_LABELS_RESPONSE_DICT = {"labels": copy.deepcopy(GET_LABELS_RESPONSE_LIST)}

REMOVE_LABEL_FROM_DOCUMENT_JSON = json.dumps(True)

CREATE_LABEL_RESPONSE_DICT = {
    "_id": "string",
    "name": "string",
}
CREATE_LABEL_RESPONSE_JSON = json.dumps(CREATE_LABEL_RESPONSE_DICT)

ADD_LABEL_ON_DOCUMENT_RESPONSE_LIST = [
    {
        "_id": "string",
        "parentId": "string",
        "title": "string",
        "state": "new",
        "files": [{"blobName": "string", "url": "string"}],
        "documentType": "string",
        "modelName": "string",
        "date": "string",
        "source": "string",
        "reviewer": {"id": "string", "email": "string", "firstName": "string", "lastName": "string"},
        "labels": [{"_id": "string", "name": "string"}],
        "language": "string",
        "engine": "string",
        "llmType": "string",
        "communication": {
            "comments": [{"text": "string", "createdAt": "2024-11-26T23:11:49.923Z", "createdBy": "string"}]
        },
        "previewDocuments": {
            "additionalProp1": {"blobName": "string", "url": "string"},
            "additionalProp2": {"blobName": "string", "url": "string"},
            "additionalProp3": {"blobName": "string", "url": "string"},
        },
        "processingDocuments": {
            "additionalProp1": {"blobName": "string", "url": "string"},
            "additionalProp2": {"blobName": "string", "url": "string"},
            "additionalProp3": {"blobName": "string", "url": "string"},
        },
        "error": {"description": "", "inState": "new"},
        "containerType": "email",
        "containerMetadata": {
            "subject": "string",
            "sender": "string",
            "recipients": ["string"],
            "cc": ["string"],
            "body": "string",
            "date": "string",
        },
        "assignedRelations": [{"type": "string", "code": "string"}],
        "assignmentStatus": "unassigned",
        "priority": "low",
    }
]
ADD_LABEL_ON_DOCUMENT_RESPONSE_JSON = json.dumps(ADD_LABEL_ON_DOCUMENT_RESPONSE_LIST)
ADD_LABEL_ON_DOCUMENT_RESPONSE_DICT = copy.deepcopy(ADD_LABEL_ON_DOCUMENT_RESPONSE_LIST)[0]

GET_STATES_RESPONSE_DICT = {"preprocessing": {"title": "Preprocessing", "name": "preprocessing"}}
GET_STATES_RESPONSE_JSON = json.dumps(GET_STATES_RESPONSE_DICT)

DOCUMENT_LIST_NO_META_RESPONSE_DICT = {
    "result": [
        {
            "_id": "string",
            "parentId": "string",
            "title": "string",
            "state": "new",
            "files": [{"blobName": "string", "url": "string"}],
            "documentType": "string",
            "modelName": "string",
            "date": "string",
            "source": "string",
            "reviewer": {"id": "string", "email": "string", "firstName": "string", "lastName": "string"},
            "labels": [{"_id": "string", "name": "string"}],
            "language": "string",
            "engine": "string",
            "llmType": "string",
            "communication": {
                "comments": [{"text": "string", "createdAt": "2024-12-09T13:27:11.293Z", "createdBy": "string"}]
            },
            "previewDocuments": {
                "additionalProp1": {"blobName": "string", "url": "string"},
                "additionalProp2": {"blobName": "string", "url": "string"},
                "additionalProp3": {"blobName": "string", "url": "string"},
            },
            "processingDocuments": {
                "additionalProp1": {"blobName": "string", "url": "string"},
                "additionalProp2": {"blobName": "string", "url": "string"},
                "additionalProp3": {"blobName": "string", "url": "string"},
            },
            "error": {"description": "", "inState": "new"},
            "containerType": "email",
            "containerMetadata": {
                "firstLevelChildCount": 1,
                "subject": "string",
                "sender": "string",
                "recipients": ["string"],
                "cc": ["string"],
                "body": "string",
                "date": "string",
            },
            "assignedRelations": [{"type": "string", "code": "string"}],
            "assignmentStatus": "unassigned",
            "priority": "low",
        }
    ]
}
DOCUMENT_LIST_NO_META_RESPONSE_JSON = json.dumps(DOCUMENT_LIST_NO_META_RESPONSE_DICT)

DOCUMENT_LIST_RESPONSE_DICT = {
    "meta": {"total": 0, "size": 0},
    "result": copy.deepcopy(DOCUMENT_LIST_NO_META_RESPONSE_DICT["result"]),
}
DOCUMENT_LIST_RESPONSE_JSON = json.dumps(DOCUMENT_LIST_RESPONSE_DICT)

DOCUMENT_DETAIL_RESPONSE_DICT = {
    "_id": "string",
    "parentId": "string",
    "title": "string",
    "state": "new",
    "files": [{"blobName": "string", "url": "string"}],
    "documentType": "string",
    "modelName": "string",
    "date": "string",
    "source": "string",
    "reviewer": {"id": "string", "email": "string", "firstName": "string", "lastName": "string"},
    "labels": [{"_id": "string", "name": "string"}],
    "language": "string",
    "engine": "string",
    "llmType": "string",
    "communication": {"comments": [{"text": "string", "createdAt": "2024-12-10T00:59:02.181Z", "createdBy": "string"}]},
    "previewDocuments": {
        "additionalProp1": {"blobName": "string", "url": "string"},
        "additionalProp2": {"blobName": "string", "url": "string"},
        "additionalProp3": {"blobName": "string", "url": "string"},
    },
    "processingDocuments": {
        "additionalProp1": {"blobName": "string", "url": "string"},
        "additionalProp2": {"blobName": "string", "url": "string"},
        "additionalProp3": {"blobName": "string", "url": "string"},
    },
    "error": {"description": "", "inState": "new"},
    "containerType": "email",
    "containerMetadata": {
        "firstLevelChildCount": 1,
        "subject": "string",
        "sender": "string",
        "recipients": ["string"],
        "cc": ["string"],
        "body": "string",
        "date": "string",
    },
    "assignedRelations": [{"type": "string", "code": "string"}],
    "assignmentStatus": "unassigned",
    "priority": "low",
}
DOCUMENT_DETAIL_RESPONSE_JSON = json.dumps(DOCUMENT_DETAIL_RESPONSE_DICT)

DOCUMENT_METADATA_RESPONSE_DICT = {"id": "string", "metadata": {"string": "string"}}
DOCUMENT_METADATA_RESPONSE_JSON = json.dumps(DOCUMENT_METADATA_RESPONSE_DICT)
