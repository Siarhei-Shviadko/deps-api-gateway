import json

AZURE_EXTRACTOR_INFO_DICT = {
    "id": "NiceId",
    "modelId": "LovelyModelId",
    "endpoint": "FabulousEndpoint",
}
AZURE_EXTRACTOR_INFO_JSON = json.dumps(AZURE_EXTRACTOR_INFO_DICT)

AZURE_EXTRACTOR_HEALTHCHECK_DICT = {
    "status": "Synchronized",
    "description": "some description",
}

AZURE_EXTRACTOR_HEALTHCHECK_JSON = json.dumps(AZURE_EXTRACTOR_HEALTHCHECK_DICT)
