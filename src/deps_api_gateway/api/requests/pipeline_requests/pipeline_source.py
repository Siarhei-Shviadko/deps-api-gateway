from enum import Enum

__all__ = ["PipelineSource"]


class PipelineSource(str, Enum):
    DOCUMENT = "document"
    WORKFLOW_MANAGER = "workflow_manager"
