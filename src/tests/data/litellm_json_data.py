import json

LITELLM_MODELS_RESPONSE_DICT = {
    "object": "list",
    "data": [{"id": "gpt-4", "object": "model", "created": 0, "owned_by": "openai"}],
}
LITELLM_MODELS_RESPONSE_JSON = json.dumps(LITELLM_MODELS_RESPONSE_DICT)
