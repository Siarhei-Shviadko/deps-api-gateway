import json

PROMPTER_MODELS_DATA_DICT = {
    "models": [
        {
            "name": "anthropic.claude",
            "code": "anthropic.claude",
        },
        {
            "name": "openai.gpt-4",
            "code": "gpt-4-0125-preview",
        },
        {
            "name": "meta.llama2",
            "code": "meta.llama2-13b-chat-v1",
        },
    ]
}

PROMPTER_MODELS_DATA_JSON = json.dumps(PROMPTER_MODELS_DATA_DICT)
