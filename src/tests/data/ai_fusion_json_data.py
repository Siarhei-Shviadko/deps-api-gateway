import json
from typing import Any
from uuid import uuid4

from deps_api_gateway.application import Cardinality, DataType
from deps_api_gateway.domain.dtos.context_attachments import ContextAttachments

AI_FUSION_COMPLETION_CREATED_RESPONSE_DATA_DICT = {
    "question": "question",
    "model": "model",
    "provider": "provider",
    "response": "response",
    "createdAt": "2021-08-31T00:00:00.000Z",
}

AI_FUSION_COMPLETION_CREATE_REQUEST = {
    "question": "question",
    "model": "model",
    "provider": "provider",
    "pageSpan": [1, 2],
    "files": ["file1.png", "file2.png"],
}

AI_FUSION_COMPLETION_CREATED_RESPONSE_JSON = json.dumps(AI_FUSION_COMPLETION_CREATED_RESPONSE_DATA_DICT)


AI_FUSION_CONVERSATION_GET_RESPONSE_DATA_DICT = {
    "conversation": {
        "entityId": "entityId",
        "tenantId": "tenantId",
        "userId": "userId",
        "completions": [
            {
                "code": "Hello",
                "question": "question",
                "model": "model",
                "provider": "provider",
                "response": "response",
                "createdAt": "2021-08-31T00:00:00.000Z",
            }
        ],
    },
    "providers": [
        {
            "code": "code",
            "name": "name",
            "models": [
                {
                    "code": "code",
                    "name": "name",
                }
            ],
        },
    ],
}

AI_FUSION_CONVERSATION_GET_RESPONSE_JSON = json.dumps(AI_FUSION_CONVERSATION_GET_RESPONSE_DATA_DICT)


AI_FUSION_AVAILABLE_MODELS_RESPONSE_DICT = {
    "providers": [
        {
            "code": "dial",
            "name": "EPAM DIAL",
            "models": [
                {"code": "code", "name": "name", "contextType": "text-based", "description": "description"},
            ],
        }
    ]
}
AI_FUSION_AVAILABLE_MODELS_RESPONSE_JSON = json.dumps(AI_FUSION_AVAILABLE_MODELS_RESPONSE_DICT)


AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_DICT = {
    "elements": {
        "code": {
            "content": "content",
            "confidence": 0.5,
        },
        "anotherCode": {
            "content": "anotherContent",
            "confidence": 0.5,
        },
    }
}
AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_JSON = json.dumps(AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_DICT)


AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT: dict[str, Any] = {
    "code": "code",
    "workflow": {
        "startNodeId": "1",
        "endNodeId": "1",
        "nodes": [{"id": "1", "name": "DefaultName", "prompt": "test_promp"}],
        "edges": [],
    },
    "shape": {"dataType": DataType.STRING.value, "cardinality": "scalar", "includeAliases": False},
}
AI_FUSION_SERIALIZED_QUERY_RESPONSE_JSON = json.dumps(AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT)
AI_FUSION_ATTACH_LLM_EXTRACTOR_REQUEST = {
    "extractorName": "TestExtractor",
    "documentTypeName": "test_llm_extraction",
    "provider": "openai",
    "model": "test_model",
    "extractionParams": {
        "customInstruction": "Give me summary",
        "groupingFactor": 2,
        "temperature": 0.4,
        "topP": 0,
        "stop": ["END", "\n"],
        "seed": 42,
        "logprobs": False,
        "extraModelParams": {"n": 5},
        "coordinatesEnabled": True,
    },
    "contextAttachments": ContextAttachments.DOCUMENT_IMAGES,
}

AI_FUSION_ATTACH_LLM_EXTRACTOR_REQUEST_WITHOUT_COORDINATES = {
    "extractorName": "TestExtractor",
    "documentTypeName": "test_llm_extraction",
    "provider": "openai",
    "model": "test_model",
    "extractionParams": {
        "customInstruction": "Give me summary",
        "groupingFactor": 2,
        "temperature": 0.4,
        "topP": 0,
        "stop": ["END", "\n"],
        "seed": 42,
        "logprobs": False,
        "extraModelParams": {"n": 5},
    },
}

AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_JSON = json.dumps(
    {"extractorId": "04d8c61728be419f80c0c6cb324e7f63", "documentTypeId": "141b4826ee4341859dbe1a85013a2569"}
)

AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_DICT = {
    "extractorId": "04d8c61728be419f80c0c6cb324e7f63",
    "documentTypeId": "141b4826ee4341859dbe1a85013a2569",
}

AI_FUSION_UPDATE_LLM_EXTRACTOR_REQUEST = {
    "name": "newname",
    "extractionParams": {
        "customInstruction": "new_instruction",
        "groupingFactor": 3,
        "temperature": 0.5,
        "topP": 0.5,
        "maxTokens": 4096,
        "stop": ["END", "\n"],
        "seed": 42,
        "logprobs": False,
        "extraModelParams": {"n": 5},
        "pageSpan": {"start": 3, "end": 5},
        "contextAttachments": ContextAttachments.DOCUMENT_IMAGES,
        "coordinatesEnabled": True,
    },
}

AI_FUSION_UPDATE_LLM_EXTRACTOR_REQUEST_WITHOUT_COORDINATES = {
    "name": "newname",
    "extractionParams": {
        "customInstruction": "new_instruction",
        "groupingFactor": 3,
        "temperature": 0.5,
        "topP": 0.5,
        "maxTokens": 4096,
        "stop": ["END", "\n"],
        "seed": 42,
        "logprobs": False,
        "extraModelParams": {"n": 5},
        "pageSpan": {"start": 3, "end": 5},
        "contextAttachments": ContextAttachments.DOCUMENT_IMAGES,
    },
}

AI_FUSION_GET_LLM_EXTRACTORS_RESPONSE_DICT = {
    "llmExtractors": [
        {
            "extractorId": "04d8c61728be419f80c0c6cb324e7f63",
            "name": "some_name",
            "llmReference": {"provider": "dial", "model": "gpt-4"},
            "extractionParams": {
                "customInstruction": "prompt",
                "groupingFactor": 5,
                "temperature": 0.5,
                "topP": 0.5,
                "coordinatesEnabled": True,
            },
            "queries": [AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT],
        },
    ],
}
AI_FUSION_GET_LLM_EXTRACTORS_RESPONSE_JSON = json.dumps(AI_FUSION_GET_LLM_EXTRACTORS_RESPONSE_DICT)

EXPECTED_LLM_EXTRACTORS_IN_DOCUMENT_TYPE_RESPONSE = [
    {
        "extractorId": "04d8c61728be419f80c0c6cb324e7f63",
        "name": "some_name",
        "llmReference": {
            "provider": "dial",
            "model": "gpt-4",
        },
        "extractionParams": {
            "customInstruction": "prompt",
            "groupingFactor": 5,
            "temperature": 0.5,
            "topP": 0.5,
            "coordinatesEnabled": True,
        },
        "queries": [AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT],
    },
]

EXPECTED_CREATE_LLM_EXTRACTOR_EXTRACTION_PARAMS = {
    "customInstruction": "Give me summary",
    "groupingFactor": 2,
    "temperature": 0.4,
    "topP": 0,
    "maxTokens": None,
    "stop": ["END", "\n"],
    "seed": 42,
    "logprobs": False,
    "extraModelParams": {"n": 5},
    "pageSpan": None,
    "contextAttachments": None,
    "coordinatesEnabled": True,
}

EXPECTED_CREATE_LLM_EXTRACTOR_EXTRACTION_PARAMS_OMITTED = {
    **EXPECTED_CREATE_LLM_EXTRACTOR_EXTRACTION_PARAMS,
    "coordinatesEnabled": False,
}

EXPECTED_UPDATE_LLM_EXTRACTOR_EXTRACTION_PARAMS = {
    "customInstruction": "new_instruction",
    "groupingFactor": 3,
    "temperature": 0.5,
    "topP": 0.5,
    "maxTokens": 4096,
    "stop": ["END", "\n"],
    "seed": 42,
    "logprobs": False,
    "extraModelParams": {"n": 5},
    "pageSpan": {"start": 3, "end": 5},
    "contextAttachments": ContextAttachments.DOCUMENT_IMAGES.value,
    "coordinatesEnabled": True,
}

EXPECTED_UPDATE_LLM_EXTRACTOR_EXTRACTION_PARAMS_OMITTED = {
    **EXPECTED_UPDATE_LLM_EXTRACTOR_EXTRACTION_PARAMS,
    "coordinatesEnabled": False,
}

AI_FUSION_CREATE_QUERY_REQUEST = {
    "code": uuid4().hex,
    "workflow": {
        "startNodeId": "123",
        "endNodeId": "123",
        "nodes": [{"id": "123", "name": uuid4().hex, "prompt": uuid4().hex}],
        "edges": [],
    },
    "shape": {"dataType": DataType.STRING, "cardinality": Cardinality.SCALAR, "includeAliases": False},
}
