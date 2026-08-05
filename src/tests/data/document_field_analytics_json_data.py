MOST_ACTIVE_FIELDS_RESPONSE = {
    "items": [
        {
            "fieldCode": "invoice_number",
            "documentTypeId": "invoice",
            "modificationCount": 5,
            "documentsWithModifications": 3,
        },
    ],
    "totalCount": 1,
}

MOST_MISSED_FIELDS_RESPONSE = {
    "items": [
        {
            "fieldCode": "total_amount",
            "documentTypeId": "invoice",
            "missCount": 2,
        },
    ],
    "totalCount": 1,
}

FIELD_ANALYTICS_RESPONSE = {
    "id": "analytics-1",
    "documentId": "doc-1",
    "fieldCode": "invoice_number",
    "documentTypeId": "invoice",
    "modifications": [],
    "miss": None,
    "modificationCount": 0,
    "hasMiss": False,
    "currentValue": None,
}

FIELD_ANALYTICS_LIST_VALUES_RESPONSE = {
    "id": "analytics-list-1",
    "documentId": "doc-list-1",
    "fieldCode": "line_items",
    "documentTypeId": "invoice",
    "modifications": [
        {
            "oldValue": [],
            "newValue": [{"item": "A"}],
            "modifiedBy": "user-1",
            "modifiedAt": "2024-01-01T00:00:00",
        },
    ],
    "miss": None,
    "modificationCount": 1,
    "hasMiss": False,
    "currentValue": [{"item": "A"}],
}

ALL_ANALYTICS_FOR_FIELD_RESPONSE = {
    "items": [
        {
            "documentId": "doc-1",
            "modificationCount": 1,
            "hasMiss": False,
            "currentValue": {"value": "123"},
            "lastModifiedBy": "user-1",
            "lastModifiedAt": "2024-01-01T00:00:00",
        },
    ],
    "totalCount": 1,
}

ALL_ANALYTICS_FOR_FIELD_LIST_VALUES_RESPONSE = {
    "items": [
        {
            "documentId": "doc-list-1",
            "modificationCount": 1,
            "hasMiss": False,
            "currentValue": [{"item": "A"}],
            "lastModifiedBy": "user-1",
            "lastModifiedAt": "2024-01-01T00:00:00",
        },
    ],
    "totalCount": 1,
}

FIELD_QUALITY_METRICS_RESPONSE = {
    "fieldCode": "invoice_number",
    "documentTypeId": "invoice",
    "documentsWithMisses": 1,
    "documentsWithModifications": 2,
    "totalModifications": 3,
}

DOCUMENT_TYPE_QUALITY_METRICS_RESPONSE = {
    "items": [
        {
            "documentTypeId": "invoice",
            "totalFieldsTracked": 50,
            "totalFieldsMissed": 2,
            "totalModifications": 5,
            "documentsWithModifications": 2,
        },
    ],
}

ANALYTIC_NOT_FOUND_ERROR = {
    "code": "not_found",
    "message": "Document field analytics not found",
}

EXTRACTION_DOCUMENT_TYPES_FOR_ANALYTICS_RESPONSE = {
    "result": [
        {
            "id": "invoice",
            "tenantId": "deps",
            "documentType": "Invoice",
            "fields": [
                {
                    "code": "invoice_number",
                    "name": "Invoice Number",
                    "fieldType": "string",
                    "fieldMeta": {},
                },
                {
                    "code": "total_amount",
                    "name": "Total Amount",
                    "fieldType": "string",
                    "fieldMeta": {},
                },
            ],
        },
    ],
}

EXTRACTION_DOCUMENT_TYPE_INVOICE_RESPONSE = {
    "id": "invoice",
    "tenantId": "deps",
    "documentType": "Invoice",
    "fields": [
        {
            "code": "invoice_number",
            "name": "Invoice Number",
            "fieldType": "string",
            "fieldMeta": {},
        },
    ],
}

MOST_ACTIVE_FIELDS_ENRICHED_RESPONSE = {
    "items": [
        {
            "fieldCode": "invoice_number",
            "documentTypeId": "invoice",
            "modificationCount": 5,
            "documentsWithModifications": 3,
            "documentTypeName": "Invoice",
            "fieldName": "Invoice Number",
        },
    ],
    "totalCount": 1,
}

MOST_MISSED_FIELDS_ENRICHED_RESPONSE = {
    "items": [
        {
            "fieldCode": "total_amount",
            "documentTypeId": "invoice",
            "missCount": 2,
            "documentTypeName": "Invoice",
            "fieldName": "Total Amount",
        },
    ],
    "totalCount": 1,
}

FIELD_ANALYTICS_ENRICHED_RESPONSE = {
    **FIELD_ANALYTICS_RESPONSE,
    "documentTypeName": "Invoice",
    "fieldName": "Invoice Number",
}

ALL_ANALYTICS_FOR_FIELD_ENRICHED_RESPONSE = {
    "items": [
        {
            "documentId": "doc-1",
            "modificationCount": 1,
            "hasMiss": False,
            "currentValue": {"value": "123"},
            "lastModifiedBy": "user-1",
            "lastModifiedAt": "2024-01-01T00:00:00",
            "documentTypeName": "Invoice",
            "fieldName": "Invoice Number",
        },
    ],
    "totalCount": 1,
    "documentTypeName": "Invoice",
    "fieldName": "Invoice Number",
}

FIELD_QUALITY_METRICS_ENRICHED_RESPONSE = {
    **FIELD_QUALITY_METRICS_RESPONSE,
    "documentTypeName": "Invoice",
    "fieldName": "Invoice Number",
}

DOCUMENT_TYPE_QUALITY_METRICS_ENRICHED_RESPONSE = {
    "items": [
        {
            "documentTypeId": "invoice",
            "totalFieldsTracked": 50,
            "totalFieldsMissed": 2,
            "totalModifications": 5,
            "documentsWithModifications": 2,
            "documentTypeName": "Invoice",
        },
    ],
}
