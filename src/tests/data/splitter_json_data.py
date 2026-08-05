FIND_ALL_SPLITTERS_RESPONSE = {
    "splitters": [
        {
            "id": "splitter-id-1",
            "groupId": "group-id-1",
            "documentTypeId": None,
            "name": "Test Splitter 1",
            "description": "A test splitter without document type",
            "splittingMode": "SECTION_BASED",
            "splittingQuery": "Split by sections",
            "llmType": "gpt-4",
            "splittingContextAttachments": [],
            "createdAt": "2024-01-01T00:00:00",
            "updatedAt": "2024-01-01T00:00:00",
        },
        {
            "id": "splitter-id-2",
            "groupId": "group-id-2",
            "documentTypeId": "doc-type-id-1",
            "name": "Test Splitter 2",
            "description": "A test splitter with document type",
            "splittingMode": "SECTION_BASED",
            "splittingQuery": "Split by sections",
            "llmType": "gpt-4",
            "splittingContextAttachments": [],
            "createdAt": "2024-01-01T00:00:00",
            "updatedAt": "2024-01-01T00:00:00",
        },
    ],
    "total": 2,
}

FIND_SPLITTERS_RESPONSE = {
    "splitters": [
        {
            "id": "splitter-id-1",
            "groupId": "group-id-1",
            "documentTypeId": "doc-type-id-1",
            "name": "Test Splitter",
            "description": "A test splitter",
            "splittingMode": "SECTION_BASED",
            "splittingQuery": "Split by sections",
            "llmType": "gpt-4",
            "splittingContextAttachments": [],
            "createdAt": "2024-01-01T00:00:00",
            "updatedAt": "2024-01-01T00:00:00",
        }
    ],
    "total": 1,
}

FIND_SPLITTER_RESPONSE = {
    "id": "splitter-id-1",
    "groupId": "group-id-1",
    "tenantId": "tenant-id-1",
    "documentTypeId": "doc-type-id-1",
    "name": "Test Splitter",
    "description": "A test splitter",
    "splittingMode": "SECTION_BASED",
    "splittingQuery": "Split by sections",
    "llmType": "gpt-4",
    "createdAt": "2024-01-01T00:00:00",
    "updatedAt": "2024-01-01T00:00:00",
}

CREATE_SPLITTER_REQUEST = {
    "groupId": "group-id-1",
    "documentTypeId": "doc-type-id-1",
    "name": "New Splitter",
    "description": "A new splitter",
    "query": "Split by sections",
    "llmType": "gpt-4",
}

CREATE_SPLITTER_RESPONSE = {
    "id": "splitter-id-new",
}

UPDATE_SPLITTER_REQUEST = {
    "name": "Updated Splitter",
    "description": "An updated splitter",
}

UPDATE_SPLITTER_RESPONSE = {
    "id": "splitter-id-1",
}
