GET_FILES_RESPONSE = {
    "meta": {"total": 2, "size": 2},
    "result": [
        {
            "id": "1",
            "tenantId": "t-1",
            "name": "report.pdf",
            "path": "/files/report.pdf",
            "state": {"status": "new", "errorMessage": None},
            "processingParams": {
                "groupId": None,
                "splittingEnabled": False,
                "classificationEnabled": False,
                "workflowParams": {"documentTypeId": None},
            },
            "createdAt": "2025-01-02T12:00:00Z",
            "updatedAt": None,
        },
        {
            "id": "2",
            "tenantId": "t-1",
            "name": "summary.pdf",
            "path": "/files/summary.pdf",
            "state": {"status": "completed", "errorMessage": None},
            "processingParams": {
                "groupId": None,
                "splittingEnabled": True,
                "classificationEnabled": True,
                "workflowParams": {"documentTypeId": "doc-type-1"},
            },
            "createdAt": "2025-01-03T12:00:00Z",
            "updatedAt": "2025-01-04T12:00:00Z",
        },
    ],
}

PROCESS_FILE_SUCCESS_RESPONSE = {"id": "file-123"}

PROCESS_FILE_ERROR_RESPONSE = {
    "code": "validation_error",
    "message": "Invalid workflow parameters",
    "details": {"field": "parsingFeatures", "error": "required field missing"},
}

CLASSIFY_FILE_SUCCESS_RESPONSE = {"id": "classified-file-789"}

CLASSIFY_FILE_ERROR_RESPONSE = {
    "code": "classification_error",
    "message": "Classification failed",
    "details": {"field": "groupId", "error": "invalid group identifier"},
}

SPLIT_FILE_SUCCESS_RESPONSE = {"id": "splitted-file-123"}

SPLIT_FILE_ERROR_RESPONSE = {
    "code": "splitting_error",
    "message": "Splitting failed",
    "details": {"field": "groupId", "error": "invalid group identifier"},
}

GET_FILE_SUCCESS_RESPONSE = {
    "id": "file-123",
    "tenantId": "t-1",
    "name": "document.pdf",
    "path": "/files/document.pdf",
    "state": {"status": "completed", "errorMessage": None},
    "processingParams": {
        "groupId": "group-456",
        "splittingEnabled": True,
        "classificationEnabled": True,
        "workflowParams": {
            "documentTypeId": "doc-type-1",
            "engine": "ai-engine",
            "language": "en",
            "llmType": "gpt-4",
            "parsingFeatures": ["ocr", "table_extraction"],
            "needsUnifier": True,
            "needsExtraction": True,
            "assignedToMe": False,
            "metadata": {"source": "api", "priority": "high"},
        },
    },
    "createdAt": "2025-01-15T10:30:00Z",
    "updatedAt": "2025-01-15T11:45:00Z",
}

GET_FILE_NOT_FOUND_RESPONSE = {
    "error": "File not found",
    "code": "FILE_NOT_FOUND",
    "message": "The requested file does not exist or you don't have access to it",
}

GET_FILE_SERVER_ERROR_RESPONSE = {
    "error": "Internal server error",
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred while retrieving the file",
}

CLASSIFY_EXISTING_FILE_ERROR_RESPONSE = {
    "code": "classification_error",
    "message": "Failed to classify existing file",
    "details": {"field": "groupId", "error": "invalid group identifier"},
}

CREATE_DOCUMENT_FROM_FILE_SUCCESS_RESPONSE = {
    "documentId": "doc-123",
    "documentName": "document.pdf",
}

CREATE_DOCUMENT_FROM_FILE_ERROR_RESPONSE = {
    "code": "document_creation_error",
    "message": "Failed to create document from file",
    "details": {"field": "documentType", "error": "document type not found"},
}

CREATE_BATCH_FROM_FILE_SUCCESS_RESPONSE = {
    "batchId": "batch-1",
    "batchName": "Test Batch",
}

CREATE_BATCH_FROM_FILE_ERROR_RESPONSE = {
    "code": "batch_creation_error",
    "message": "Failed to create batch from file",
    "details": {"field": "name", "error": "files path not found"},
}

RESTART_FILE_SUCCESS_RESPONSE = {
    "message": "File restarted successfully",
}

RESTART_FILE_ERROR_RESPONSE = {
    "code": "restart_error",
    "message": "Failed to restart file",
    "details": {"field": "fileId", "error": "invalid file identifier"},
}
