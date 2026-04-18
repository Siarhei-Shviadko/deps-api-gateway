from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedGroupInfo"]


class SerializedGroupInfo(ConfiguredBaseModel):
    group_id: str = Field(alias="groupId")
    group_name: str = Field(alias="groupName")
