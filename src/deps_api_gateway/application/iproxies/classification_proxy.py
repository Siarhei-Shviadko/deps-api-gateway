from typing import Optional, Protocol

from deps_api_gateway.application.proxy_response import ProxyResponse

__all__ = ["IClassificationProxy"]


class IClassificationProxy(Protocol):
    async def create_gen_ai_classifier(
        self,
        group_id: str,
        document_type_id: str,
        prompt: str,
        llm_type: str,
        name: str,
    ) -> ProxyResponse:
        pass

    async def update_gen_ai_classifier(
        self,
        gen_ai_classifier_id: str,
        prompt: Optional[str],
        llm_type: Optional[str],
        name: Optional[str],
    ) -> ProxyResponse:
        pass

    async def delete_gen_ai_classifiers(self, ids: list[str]) -> ProxyResponse:
        pass

    async def get_gen_ai_classifiers_of_group(self, group_id: str) -> ProxyResponse:
        pass

    async def get_gen_ai_classifiers_of_document_type(self, document_type_id: str) -> ProxyResponse:
        pass
