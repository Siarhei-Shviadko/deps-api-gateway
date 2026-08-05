import json
import uuid

CREATE_GEN_AI_CLASSIFIER_RESPONSE_DICT = {"id": uuid.uuid4().hex}
CREATE_GEN_AI_CLASSIFIER_RESPONSE_JSON = json.dumps(CREATE_GEN_AI_CLASSIFIER_RESPONSE_DICT)


GET_CLASSIFIERS_OF_GROUP_RESPONSE_DICT = {
    "genAiClassifiers": [
        {
            "genAiClassifierId": "genAiClassifierId",
            "documentTypeId": "documentTypeId",
            "prompt": "prompt",
            "llmType": "llmType",
            "name": "name",
        }
    ]
}
GET_CLASSIFIERS_OF_GROUP_RESPONSE_JSON = json.dumps(GET_CLASSIFIERS_OF_GROUP_RESPONSE_DICT)

GET_CLASSIFIERS_OF_DOCUMENT_TYPE_RESPONSE_DICT = {
    "genAiClassifiers": [
        {
            "genAiClassifierId": "genAiClassifierId",
            "documentTypeId": "documentTypeId",
            "prompt": "prompt",
            "llmType": "llmType",
            "name": "name",
        }
    ]
}
GET_CLASSIFIERS_OF_DOCUMENT_TYPE_RESPONSE_JSON = json.dumps(GET_CLASSIFIERS_OF_DOCUMENT_TYPE_RESPONSE_DICT)

GET_GROUP_RESPONSE_DICT = {"group": {"id": "id", "name": "name", "documentTypeIds": ["documentTypeId"]}}
GET_GROUP_RESPONSE_JSON = json.dumps(GET_GROUP_RESPONSE_DICT)
