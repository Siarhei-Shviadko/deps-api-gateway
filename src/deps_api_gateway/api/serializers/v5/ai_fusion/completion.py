from datetime import datetime
from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedCompletion", "CreateCompletionRequest"]


class CreateCompletionRequest(ConfiguredBaseModel):
    question: str
    model: str
    provider: str
    page_span: Optional[tuple[int, int]] = Field(default=None, alias="pageSpan")
    files: Optional[list[str]] = Field(default=None)


class SerializedCompletion(ConfiguredBaseModel):
    code: str
    question: str
    response: str
    model: str
    provider: str
    confidence: Optional[float]
    created_at: datetime = Field(..., alias="createdAt")
