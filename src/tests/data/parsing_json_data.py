import json
import uuid
from datetime import UTC, datetime

from faker import Faker

fake = Faker()


DOCUMENT_LAYOUT_DICT = {
    "documentLayoutId": uuid.uuid4().hex,
    "parsingFeatures": {"GCP_VISION": ["tables"]},
    "pages": [
        {
            "id": uuid.uuid4().hex,
            "pageNumber": 0,
            "parsingType": "GCP_VISION",
            "dimension": {"width": 0, "height": 0, "unit": "px"},
            "languages": [{"languageCode": "eng", "confidence": 1.0}],
            "filePath": fake.uri_path(),
            "transformations": {
                "thresholding": {"lowValue": 2, "highValue": 2, "flag": 2},
                "blurring": {"kernel": [2, 2], "sigma": 1.0},
            },
            "images": [
                {
                    "id": uuid.uuid4().hex,
                    "order": 0,
                    "title": "title",
                    "filePath": fake.uri_path(),
                    "polygon": [{"x": 0.0, "y": 0.0}],
                    "description": uuid.uuid4().hex,
                }
            ],
            "paragraphs": [
                {
                    "id": uuid.uuid4().hex,
                    "order": 2,
                    "content": "content",
                    "confidence": 1.0,
                    "role": "HEADER",
                    "polygon": [{"x": 0.0, "y": 0.0}],
                    "lines": [
                        {
                            "order": 0,
                            "content": "content",
                            "confidence": 1.0,
                            "polygon": [{"x": 0.0, "y": 0.0}],
                            "words": [
                                {
                                    "order": 0,
                                    "confidence": 1.0,
                                    "polygon": [{"x": 0.0, "y": 0.0}],
                                    "content": "content",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": False,
                                        "italic": False,
                                        "handwritten": False,
                                        "fontType": "Arial",
                                        "fontSize": "12pt",
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": False,
                                    },
                                }
                            ],
                            "selectionMarks": [
                                {"order": 1, "confidence": 1.0, "polygon": [{"x": 0.0, "y": 0.0}], "state": "state"}
                            ],
                            "barcodes": [
                                {
                                    "order": 2,
                                    "confidence": 1.0,
                                    "polygon": [{"x": 0.0, "y": 0.0}],
                                    "value": "value",
                                    "kind": "kind",
                                }
                            ],
                            "formulas": [
                                {
                                    "order": 3,
                                    "confidence": 1.0,
                                    "polygon": [{"x": 0.0, "y": 0.0}],
                                    "value": "value",
                                    "kind": "kind",
                                }
                            ],
                            "signatures": [
                                {"order": 4, "confidence": 1.0, "polygon": [{"x": 0.0, "y": 0.0}], "value": "value"}
                            ],
                        }
                    ],
                }
            ],
            "tables": [
                {
                    "id": uuid.uuid4().hex,
                    "order": 1,
                    "confidence": 1.0,
                    "columnCount": 1,
                    "rowCount": 1,
                    "polygon": [{"x": 0.0, "y": 0.0}],
                    "cells": [
                        {
                            "content": "string",
                            "columnIndex": 1,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [{"x": 0.0, "y": 0.0}],
                            "paragraphId": uuid.uuid4().hex,
                        }
                    ],
                }
            ],
            "keyValuePairs": [
                {
                    "id": uuid.uuid4().hex,
                    "key": {"content": "key", "polygon": [{"x": 0, "y": 0}], "paragraphId": uuid.uuid4().hex},
                    "value": {"content": "value", "polygon": [{"x": 0, "y": 0}], "paragraphId": uuid.uuid4().hex},
                    "confidence": 1.0,
                    "order": 0,
                }
            ],
            "groups": [{"id": "string", "name": "string", "members": ["string"]}],
        }
    ],
}
DOCUMENT_LAYOUT_JSON = json.dumps(DOCUMENT_LAYOUT_DICT)


PARSING_INFO_DICT = {
    "layoutId": "a6f2b250361a4813b46dfdbcde231dab",
    "documentLayoutInfo": {
        "documentLayoutId": "a6f2b250361a4813b46dfdbcde231dab",
        "parsingFeatures": {"AZURE_FORM_RECOGNIZER": ["tables", "images"]},
        "pagesInfo": {"AZURE_FORM_RECOGNIZER": {"pagesCount": 20}},
    },
    "tabularLayoutInfo": {
        "id": "a6f2b250361a4813b46dfdbcde231dab",
        "parsingType": "CSV",
        "sheets": [
            {
                "id": "cdc62593e3414a429f268355ebb6857e",
                "title": "a4ee8a19ad9842a69ec8c096419a5aa5",
                "isHidden": False,
                "tables": [{"id": "a1489d97d73040ed94f8679bbb77a3a6", "rowCount": 10, "columnCount": 10}],
                "images": ["ef0961fa20f34daaa3c6e831f43373f8"],
            },
            {
                "id": "ecbc221ce52f4f28b64d10b9a97bbf2a",
                "title": "411d32c2bbea47f396e9cddd640ab981",
                "isHidden": False,
                "tables": [{"id": "f6e06f86cb93491380e9d86c1b9d532f", "rowCount": 5, "columnCount": 5}],
                "images": ["ac8805c15fcc4a02bcf13e19c5961a2b"],
            },
        ],
    },
}

PARSING_INFO_JSON = json.dumps(PARSING_INFO_DICT)

TABULAR_LAYOUT_DICT = {
    "id": "test_doc_id",
    "tenant_id": "test_tenant_id",
    "parsing_type": "EXCEL",
    "extracted_properties": ["STYLING", "ALIGNMENT", "COMMENTS", "BORDERS"],
    "sheets": {
        "540714947c114c1ea8ec68e5923606a5": {
            "id": "540714947c114c1ea8ec68e5923606a5",
            "title": "tables",
            "isHidden": False,
            "images": [],
            "table_ids": ["78d90ec1a342471ea2587ffb12a7c799"],
        }
    },
    "tables": {
        "78d90ec1a342471ea2587ffb12a7c799": {
            "schema": {
                "id": "78d90ec1a342471ea2587ffb12a7c799",
                "sheet_id": "540714947c114c1ea8ec68e5923606a5",
                "column_count": 1,
                "row_count": 1,
                "placement": [{"row": 18, "column": 1}, {"row": 18, "column": 1}],
            },
            "data": [
                {
                    "id": "b8d046a2e0aa4647bb8db3486f9852d9",
                    "tableId": "78d90ec1a342471ea2587ffb12a7c799",
                    "content": "TEST CONTENT",
                    "dataType": "NUMERIC",
                    "relativePosition": [0, 0],
                    "absolutePosition": [1, 18],
                    "merge": None,
                    "style": {
                        "backgroundColor": "00000000",
                        "color": "Values must be of type <class 'str'>",
                        "hyperlink": False,
                        "bold": False,
                        "italic": False,
                        "fontName": "Calibri",
                        "fontSize": "11.0",
                        "underlined": False,
                        "strikethrough": None,
                    },
                    "comment": None,
                    "alignment": {"horizontal": None, "vertical": None, "rotation": 0},
                    "borders": {"top": None, "bottom": None, "left": None, "right": None},
                }
            ],
        }
    },
}

TABULAR_LAYOUT_JSON = json.dumps(TABULAR_LAYOUT_DICT)


SEMANTIC_LAYOUT_DICT = {
    "id": uuid.uuid4().hex,
    "createdAt": datetime.now(UTC).isoformat(),
    "metadata": {
        "sourceProvider": uuid.uuid4().hex,
        "processingTimeMs": 100,
        "confidence": 0.99,
    },
    "sections": [
        {
            "id": uuid.uuid4().hex,
            "order": 0,
            "title": uuid.uuid4().hex,
            "contentElements": [
                {
                    "id": uuid.uuid4().hex,
                    "order": 0,
                    "type": uuid.uuid4().hex,
                    "content": {
                        "markdown": uuid.uuid4().hex,
                    },
                }
            ],
        }
    ],
}

SEMANTIC_LAYOUT_JSON = json.dumps(SEMANTIC_LAYOUT_DICT)


EDIT_IMAGE_REQUEST_DICT = {
    "title": "New Image Title",
    "description": "New Image Description",
    "filepath": "/new/path/to/image.jpg",
    "polygon": [{"x": 0.1, "y": 0.1}, {"x": 0.2, "y": 0.2}],
}
