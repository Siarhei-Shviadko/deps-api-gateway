from deps_api_gateway.constants import (
    DOCUMENT_BASE_API_PREFIX,
    EXTRACTION_TYPE_PLACEHOLDER,
    V1_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)

from .generic_pipeline import GenericPipelineRequest

__all__ = ["RunPipelineRequest"]


class RunPipelineRequest(GenericPipelineRequest):
    DOCUMENT_PIPELINE_URI = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/run-pipeline"
    WORKFLOW_PIPELINE_URI = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/run-{EXTRACTION_TYPE_PLACEHOLDER}-pipeline"
