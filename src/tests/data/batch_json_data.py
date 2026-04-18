from datetime import datetime

BATCH_CREATE_REQUEST = {
    "name": "Test Batch",
    "groupId": "0",
    "metadata": None,
    "files": [
        {
            "name": "test.pdf",
            "path": "/test.pdf",
            "documentTypeId": None,
            "processingParams": {
                "engine": "Tesseract",
                "language": "English",
                "llmType": "EPAM DIAL",
                "parsingFeatures": ["text", "images"],
            },
        }
    ],
}

GET_BATCHES_RESPONSE = {
    "meta": {"total": 5, "size": 2},
    "result": [
        {
            "id": "1",
            "name": "1",
            "group": "1",
            "status": "new",
            "files": [{"name": "1", "status": "new", "error": None}],
            "createdAt": str(datetime.now()),
        },
        {
            "id": "2",
            "name": "2",
            "group": "2",
            "status": "new",
            "files": [{"name": "2", "status": "new", "error": None}],
            "createdAt": str(datetime.now()),
        },
    ],
}

GET_BATCH_INFO = {
    "id": "cedd3ef19a4a4d17a5580f5b1d7c4c24",
    "name": "aaa",
    "status": "new",
    "group": None,
    "createdAt": "2025-04-15T13:38:15.210272+00:00",
    "files": [
        {
            "id": "5b9b634eee28474f8345088bb3ec4ce1",
            "name": "aaa.pdf",
            "status": "new",
            "document_type_id": None,
            "engine": None,
            "llm_type": None,
            "parsing_features": None,
        }
    ],
}

ADD_BATCH_FILES_REQUEST = {
    "files": [
        {
            "name": "test.pdf",
            "path": "/test.pdf",
            "documentTypeId": None,
            "processingParams": {
                "engine": "Tesseract",
                "language": "English",
                "llmType": "EPAM DIAL",
                "parsingFeatures": ["text", "images"],
            },
        },
        {
            "name": "test1.pdf",
            "path": "/test1.pdf",
            "documentTypeId": None,
            "processingParams": {
                "engine": "Tesseract",
                "language": "English",
                "llmType": "EPAM DIAL",
                "parsingFeatures": ["text", "images"],
            },
        },
    ],
}
