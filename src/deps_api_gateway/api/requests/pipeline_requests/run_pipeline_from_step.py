from deps_api_gateway.constants import (
    DOCUMENT_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)

from .generic_pipeline import GenericPipelineRequest

__all__ = ["RunPipelineFromStepRequest"]


class RunPipelineFromStepRequest(GenericPipelineRequest):
    DOCUMENT_PIPELINE_URI = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/run-pipeline-from-step"
    WORKFLOW_PIPELINE_URI = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V2_PREFIX}/run-pipeline-from-step"
