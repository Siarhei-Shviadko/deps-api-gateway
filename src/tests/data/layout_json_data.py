import json

LAYOUTS_RESPONSE_DICT = {
    "reference_layouts": [
        {
            "id": "a755b8378eef437297d70f96c6c53e08",
            "prototypeId": "c910e94fd653407ea3edb94d6ea57a92",
            "state": "New",
            "title": "test1",
            "blobName": "blob_name1",
        },
        {
            "id": "61f551da4b6b405fa87055e23a6f716c",
            "prototypeId": "c910e94fd653407ea3edb94d6ea57a92",
            "state": "New",
            "title": "test2",
            "blobName": "blob_name2",
        },
    ]
}
LAYOUTS_RESPONSE_JSON = json.dumps(LAYOUTS_RESPONSE_DICT)
NO_LAYOUTS_RESPONSE_DICT = {"reference_layouts": []}  # type: ignore
NO_LAYOUTS_RESPONSE_JSON = json.dumps(NO_LAYOUTS_RESPONSE_DICT)

LAYOUT_WITH_UNIFIED_DATA_AND_DOCUMENT_LAYOUT_RESPONSE_DICT = {
    "id": "1",
    "prototypeId": "2",
    "state": "Ready",
    "title": "test",
    "blobName": "test.pdf",
    "unifiedData": {
        "documentId": "1",
        "elements": [
            {
                "id": "3",
                "page": 1,
                "blobName": "test/original/0.png",
                "width": 2481,
                "height": 3508,
                "appliedTransformation": None,
                "originalImageId": None,
            },
            {
                "id": "4",
                "imageId": "3",
                "page": 1,
                "wordboxes": [
                    {
                        "word": {"content": "Holiday", "confidence": 1},
                        "bbox": {
                            "x": 0.38420168067226895,
                            "y": 0.03330368608799055,
                            "w": 0.05710426890756298,
                            "h": 0.009560047562425636,
                        },
                    },
                    {
                        "word": {"content": "Inn", "confidence": 1},
                        "bbox": {
                            "x": 0.44594574789915964,
                            "y": 0.03330368608799055,
                            "w": 0.02661983193277312,
                            "h": 0.009560047562425636,
                        },
                    },
                ],
            },
        ],
    },
    "documentLayoutData": {"documentLayoutId": "1", "parsingFeatures": {}, "pages": []},
}
LAYOUT_WITH_UNIFIED_DATA_AND_DOCUMENT_LAYOUT_RESPONSE_JSON = json.dumps(
    LAYOUT_WITH_UNIFIED_DATA_AND_DOCUMENT_LAYOUT_RESPONSE_DICT,
)
LAYOUT_NOT_FOUND_RESPONSE_DICT = {
    "code": "not_found_error",
    "message": "Can't find reference layout.",
}
LAYOUT_NOT_FOUND_RESPONSE_JSON = json.dumps(LAYOUT_NOT_FOUND_RESPONSE_DICT)
