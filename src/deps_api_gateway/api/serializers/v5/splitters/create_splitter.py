from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["CreateSplitterRequest", "CreateSplitterResponse"]


class CreateSplitterRequest(ConfiguredBaseModel):
    group_id: str
    document_type_id: Optional[str] = Field(None)
    name: str
    description: Optional[str] = None
    query: str
    llm_type: str
    splitting_context_attachments: Optional[list[str]] = None
    mode: Optional[str] = None


class CreateSplitterResponse(ConfiguredBaseModel):
    id: str
