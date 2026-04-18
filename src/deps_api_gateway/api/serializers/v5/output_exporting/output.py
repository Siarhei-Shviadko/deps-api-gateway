from datetime import datetime

from ...base import ConfiguredBaseModel
from .profile_info import ProfileInfoResponse

__all__ = ["SerializedOutput", "BuildOutputRequest"]


class SerializedOutput(ConfiguredBaseModel):
    id: str
    tenant_id: str
    profile_info: ProfileInfoResponse
    document_id: str
    state: str
    file_path: str
    creation_date: datetime


class BuildOutputRequest(ConfiguredBaseModel):
    document_type_id: str
    profile_id: str
