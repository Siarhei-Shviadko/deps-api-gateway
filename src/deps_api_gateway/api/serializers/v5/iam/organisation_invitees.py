from ...base import ConfiguredBaseModel
from .invitation import SerializedInvitation
from .list_metadata import ListMetadata

__all__ = ["GetOrganisationInviteesResponse"]


class GetOrganisationInviteesResponse(ConfiguredBaseModel):
    meta: ListMetadata
    result: list[SerializedInvitation]
