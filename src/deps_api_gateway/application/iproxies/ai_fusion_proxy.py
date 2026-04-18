from typing import Any, Optional, Protocol, Union

from deps_api_gateway.domain import ContextAttachments

from ..proxy_response import ProxyResponse
from ..types import InsightsRequestParamsDict, RawDataShape, RawLLMWorkflow

__all__ = ["IAIFusionProxy"]


class IAIFusionProxy(Protocol):
    async def create_completion(
        self,
        entity_id: str,
        model: str,
        provider: str,
        question: str,
        page_span: Optional[tuple[int, int]] = None,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        ...

    async def remove_completions(self, entity_id: str, completion_codes: list[str]) -> ProxyResponse:
        ...

    async def get_conversation(self, entity_id: str) -> ProxyResponse:
        ...

    async def clear_conversation(self, entity_id: str) -> ProxyResponse:
        ...

    async def get_available_models(self) -> ProxyResponse:
        ...

    async def retrieve_insights(
        self,
        document_id: str,
        model: str,
        requested_insights: dict[str, Union[str, dict[str, Any]]],
        params: InsightsRequestParamsDict,
        custom_instructions: Optional[str] = None,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        ...

    async def retrieve_file_insights(
        self,
        filepath: str,
        model: str,
        requested_insights: dict[str, Union[str, dict[str, Any]]],
        params: InsightsRequestParamsDict,
        custom_instructions: Optional[str] = None,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        ...

    async def add_extraction_query(
        self,
        extractor_id: str,
        document_type_id: str,
        code: str,
        shape: RawDataShape,
        workflow: RawLLMWorkflow,
    ) -> ProxyResponse:
        ...

    async def update_extraction_query(
        self,
        extractor_id: str,
        document_type_id: str,
        code: str,
        workflow: RawLLMWorkflow,
    ) -> ProxyResponse:
        ...

    async def create_llm_extractor(
        self,
        extractor_name: str,
        document_type_name: str,
        provider: str,
        model: str,
        extractor_id: Optional[str] = None,
        extraction_params: Optional[dict[str, Any]] = None,
    ) -> ProxyResponse:
        ...

    async def update_llm_extractor(
        self,
        extractor_id: str,
        document_type_id: str,
        name: str,
        custom_instruction: str,
        grouping_factor: int,
        temperature: float,
        top_p: float,
        page_span: Optional[dict[str, int]],
        context_attachments: Optional[ContextAttachments],
    ) -> ProxyResponse:
        ...

    async def assign_llm_to_llm_extractor(
        self,
        extractor_id: str,
        document_type_id: str,
        provider: str,
        model: str,
    ) -> ProxyResponse:
        ...

    async def get_llm_extractors(self, document_type_id: str) -> ProxyResponse:
        ...

    async def move_queries_between_extractors(
        self,
        source_extractor_id: str,
        target_extractor_id: str,
        document_type_id: str,
        fields_codes: list[str],
    ) -> ProxyResponse:
        ...

    async def add_llm_coordinates(
        self,
        entity_id: str,
        field_codes: list[str],
    ) -> ProxyResponse:
        ...
