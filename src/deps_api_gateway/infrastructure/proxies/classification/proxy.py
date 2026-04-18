from typing import Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    IClassificationProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import CLASSIFICATION_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import ClassificationServiceUnavailableError

__all__ = ["ClassificationProxy"]


class ClassificationProxy(GenericRestClient, IClassificationProxy):
    exception = ClassificationServiceUnavailableError
    v1_prefix = f"{CLASSIFICATION_BASE_API_PREFIX}{V1_PREFIX}"

    async def create_gen_ai_classifier(
        self,
        group_id: str,
        document_type_id: str,
        prompt: str,
        llm_type: str,
        name: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/gen-ai-classifiers"

        data = {
            "groupId": group_id,
            "documentTypeId": document_type_id,
            "prompt": prompt,
            "llm_type": llm_type,
            "name": name,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def update_gen_ai_classifier(
        self,
        gen_ai_classifier_id: str,
        prompt: Optional[str],
        llm_type: Optional[str],
        name: Optional[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/gen-ai-classifiers/{gen_ai_classifier_id}"

        data = {}
        if prompt is not None:
            data["prompt"] = prompt
        if llm_type is not None:
            data["llm_type"] = llm_type
        if name is not None:
            data["name"] = name

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

    async def delete_gen_ai_classifiers(self, ids: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/gen-ai-classifiers"

        data = {"id": ids}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, params=data)
            )

    async def get_gen_ai_classifiers_of_group(self, group_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups/{group_id}/gen-ai-classifiers"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def get_gen_ai_classifiers_of_document_type(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/gen-ai-classifiers"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
