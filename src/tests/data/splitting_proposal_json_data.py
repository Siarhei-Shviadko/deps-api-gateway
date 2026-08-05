GET_PROPOSAL_RESPONSE = {
    "id": "proposal-id-1",
    "tenantId": "tenant-id-1",
    "status": "pending",
    "segments": [
        {
            "name": "Segment 1",
            "contentRegions": [{"pageNumber": 1, "boundingBox": None}],
        }
    ],
    "totalPages": 3,
    "createdAt": "2024-01-01T00:00:00",
    "updatedAt": "2024-01-01T00:00:00",
    "errorMessage": None,
}

UPDATE_PROPOSAL_REQUEST = {
    "segments": [
        {
            "name": "Segment 1",
            "contentRegions": [{"pageNumber": 1, "boundingBox": None}],
        }
    ]
}
