from typing import Optional

from ...base import ConfiguredBaseModel

__all__ = ["UpdateSplitterRequest", "UpdateSplitterResponse"]


class UpdateSplitterRequest(ConfiguredBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    query: Optional[str] = None
    llm_type: Optional[str] = None
    splitting_context_attachments: Optional[list[str]] = None


class UpdateSplitterResponse(ConfiguredBaseModel):
    id: str
