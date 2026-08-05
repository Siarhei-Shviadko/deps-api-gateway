from datetime import datetime
from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["FindSplitterResponse"]


class FindSplitterResponse(ConfiguredBaseModel):
    id: str
    group_id: str
    tenant_id: str
    document_type_id: Optional[str] = Field(None)
    name: str
    description: Optional[str] = None
    splitting_mode: str
    splitting_query: str
    llm_type: str
    splitting_context_attachments: list[str]
    created_at: datetime
    updated_at: datetime
