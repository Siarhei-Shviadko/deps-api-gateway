from datetime import datetime
from typing import Optional

from fastapi.params import Query
from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["FindSplitterForRequest", "FindSplitterForResponse"]


class FindSplitterForRequest(ConfiguredBaseModel):
    group_id: str = Query(..., alias="groupId")
    document_type_id: Optional[str] = Query(default=None, alias="documentTypeId")


class FindSplitterForResponse(ConfiguredBaseModel):
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
