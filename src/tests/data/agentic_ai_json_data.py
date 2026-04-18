GET_AGENT_VENDORS_RESPONSE = {
    "agentVendors": [
        {
            "id": "fb7d01276a414207968dd45e154345f9",
            "name": "test1",
            "description": "desc1",
            "avatarUrl": None,
            "connectionParameters": {"baseUrl": "http://localhost:8000"},
        },
        {
            "id": "0c0198d014d74271b35e75885b372c7a",
            "name": "test2",
            "description": "desc2",
            "avatarUrl": "http://abc:8888",
            "connectionParameters": {"baseUrl": "http://localhost:8001"},
        },
    ]
}


GET_CONVERSATION_COMPLETIONS_RESPONSE = {
    "completions": [
        {
            "id": "cmp_0005",
            "question": {
                "text": "Generate a short bio for a product manager.",
                "createdAt": "2025-10-27T10:20:00+00:00",
            },
            "executionContext": [{"text": "team-directory"}, {"text": "linkedin-scrape-2025"}],
            "answer": {
                "text": "Product manager with 8 years of experience in SaaS and a focus on user-centered design.",
                "createdAt": "2025-10-27T10:20:03+00:00",
            },
        },
        {
            "id": "cmp_0006",
            "question": {
                "text": "What are the breaking changes in library X v2?",
                "createdAt": "2025-10-27T10:25:00+00:00",
            },
            "executionContext": [{"text": "changelog-v2"}, {"text": "migration-guide"}],
            "answer": None,
        },
    ],
    "metadata": {"size": 2, "total": 10},
}
