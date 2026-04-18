import json
from uuid import uuid4

DOCUMENT_TYPE_ID = uuid4().hex
WORKFLOW_CONFIGURATION_RESPONSE_DICT = {
    "documentTypeId": DOCUMENT_TYPE_ID,
    "parsingFeatures": ["tables"],
    "needsPostprocessing": True,
    "needsValidation": True,
    "needsReview": "always_review",
    "needsOutputExporting": True,
}
WORKFLOW_CONFIGURATION_RESPONSE_JSON = json.dumps(WORKFLOW_CONFIGURATION_RESPONSE_DICT)

WORKFLOW_CONFIGURATIONS_RESPONSE_DICT = {DOCUMENT_TYPE_ID: WORKFLOW_CONFIGURATION_RESPONSE_DICT}
WORKFLOW_CONFIGURATIONS_RESPONSE_JSON = json.dumps(WORKFLOW_CONFIGURATIONS_RESPONSE_DICT)
