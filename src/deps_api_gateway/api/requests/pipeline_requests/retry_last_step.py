from typing import Any, Optional

from deps_api_gateway.constants import (
    DOCUMENT_BASE_API_PREFIX,
    EXTRACTION_TYPE_PLACEHOLDER,
    V1_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)

from .generic_pipeline import GenericPipelineRequest
from .pipeline_source import PipelineSource

__all__ = ["RetryLastStepRequest"]


class RetryLastStepRequest(GenericPipelineRequest):
    DOCUMENT_PIPELINE_URI = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/retry-last-step"
    WORKFLOW_PIPELINE_URI = (
        f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/retry-{EXTRACTION_TYPE_PLACEHOLDER}-pipeline-last-step"
    )

    async def update_request(self, source: PipelineSource, extraction_type: Optional[str], *args, **kwargs) -> None:
        await self._create_request(source, extraction_type)

    async def _prepare_data(self) -> dict[str, Any]:
        return await self.original_request.json_data
