from ...base import ConfiguredBaseModel
from .list_metadata import ListMetadata
from .user import SerializedUser

__all__ = ["GetOrganisationUsersResponse"]


class GetOrganisationUsersResponse(ConfiguredBaseModel):
    meta: ListMetadata
    result: list[SerializedUser]
