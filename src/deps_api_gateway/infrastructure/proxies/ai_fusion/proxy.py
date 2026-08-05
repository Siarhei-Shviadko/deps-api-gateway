from typing import Any, Optional, Union

from async_rest_client import Methods

from deps_api_gateway.application import (
    IAIFusionProxy,
    InsightsRequestParamsDict,
    ProxyResponse,
    ProxyResponseFactory,
    RawDataShape,
    RawLLMWorkflow,
)
from deps_api_gateway.constants import AI_FUSION_BASE_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import AIFusionError, AIFusionServiceUnavailableError

__all__ = ["AIFusionProxy"]


class AIFusionProxy(GenericRestClient, IAIFusionProxy):
    v1_prefix = f"{AI_FUSION_BASE_PREFIX}{V1_PREFIX}"
    exception = AIFusionError

    async def create_completion(
        self,
        entity_id: str,
        model: str,
        provider: str,
        question: str,
        page_span: Optional[tuple[int, int]] = None,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/conversations/{entity_id}"

        data = {
            "question": question,
            "model": model,
            "provider": provider,
            "pageSpan": {"start": page_span[0], "end": page_span[1]} if page_span else None,
            "files": files,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def remove_completions(self, entity_id: str, completion_codes: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/conversations/{entity_id}/completions"

        data = {"completionCodes": completion_codes}

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, params=data)
            )
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def get_conversation(self, entity_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/conversations/{entity_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def clear_conversation(self, entity_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/conversations/{entity_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def get_available_models(self) -> ProxyResponse:
        url = f"{self.v1_prefix}/analysis/models"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def retrieve_insights(
        self,
        document_id: str,
        model: str,
        requested_insights: dict[str, Union[str, dict[str, Any]]],
        params: InsightsRequestParamsDict,
        custom_instructions: Optional[str] = None,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/analysis/retrieve-insights"

        data = {
            "documentId": document_id,
            "model": model,
            "requestedInsights": requested_insights,
            "customInstructions": custom_instructions,
            "params": params,
            "files": files,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def retrieve_file_insights(
        self,
        filepath: str,
        model: str,
        requested_insights: dict[str, Union[str, dict[str, Any]]],
        params: InsightsRequestParamsDict,
        custom_instructions: Optional[str] = None,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/analysis/retrieve-file-insights"

        data = {
            "filePath": filepath,
            "model": model,
            "requestedInsights": requested_insights,
            "customInstructions": custom_instructions,
            "params": params,
            "files": files,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def add_extraction_query(
        self,
        extractor_id: str,
        document_type_id: str,
        code: str,
        shape: RawDataShape,
        workflow: RawLLMWorkflow,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/llm-extractors/{extractor_id}/query"

        data = {"code": code, "shape": shape, "workflow": workflow}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def update_extraction_query(
        self,
        extractor_id: str,
        document_type_id: str,
        code: str,
        workflow: RawLLMWorkflow,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/llm-extractors/{extractor_id}/query/{code}"

        data = {"workflow": workflow}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))
        except Exception as error:
            raise AIFusionServiceUnavailableError(error)

    async def create_llm_extractor(
        self,
        extractor_name: str,
        document_type_name: str,
        provider: str,
        model: str,
        extractor_id: Optional[str] = None,
        extraction_params: Optional[dict[str, Any]] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/llm-extractors"
        data = {
            "extractorName": extractor_name,
            "documentTypeName": document_type_name,
            "provider": provider,
            "model": model,
            "extractionParams": extraction_params or {},
            "extractorId": extractor_id,
        }

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def update_llm_extractor(
        self,
        extractor_id: str,
        document_type_id: str,
        name: str,
        extraction_params: dict[str, Any],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/llm-extractors/{extractor_id}"
        data = {
            "name": name,
            "extractionParams": extraction_params,
        }
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))

    async def assign_llm_to_llm_extractor(
        self,
        extractor_id: str,
        document_type_id: str,
        provider: str,
        model: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/llm-extractors/{extractor_id}/llm"
        data = {
            "provider": provider,
            "model": model,
        }
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))

    async def get_llm_extractors(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/llm-extractors"

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def move_queries_between_extractors(
        self,
        source_extractor_id: str,
        target_extractor_id: str,
        document_type_id: str,
        fields_codes: list[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/llm-extractors/move-queries"
        data = {
            "sourceExtractorId": source_extractor_id,
            "targetExtractorId": target_extractor_id,
            "fieldsCodes": fields_codes,
        }
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def add_llm_coordinates(
        self,
        entity_id: str,
        field_codes: list[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/llm-coordinates/{entity_id}"
        data = {"fieldCodes": field_codes}

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
