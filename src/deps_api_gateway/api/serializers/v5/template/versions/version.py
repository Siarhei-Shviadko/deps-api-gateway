from datetime import datetime
from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel
from .reference_page import SerializedReferencePage

__all__ = ["SerializedTemplateVersion"]


class SerializedTemplateVersion(ConfiguredBaseModel):
    id: str
    name: str
    created_at: datetime = Field(..., alias="createdAt")
    template_id: str = Field(..., alias="templateId")
    original_files: list[str] = Field(alias="originalFiles", default_factory=list)
    reference_pages: list[SerializedReferencePage] = Field(alias="referencePages", default_factory=list)
    description: Optional[str] = None
