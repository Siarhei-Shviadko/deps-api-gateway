from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["CreateGroupRequest", "CreateGroupResponse"]


class CreateGroupRequest(ConfiguredBaseModel):
    name: str
    document_type_ids: list[str] = Field(..., alias="documentTypeIds")


class CreateGroupResponse(ConfiguredBaseModel):
    id: str
