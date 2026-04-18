from enum import Enum
from typing import Union

from ...base import ConfiguredBaseModel

__all__ = ["ExternalStorageInfo", "ExternalStorageCode", "Credentials"]


class ExternalStorageCode(str, Enum):
    SALESFORCE = "Salesforce"
    ONE_DRIVE = "One Drive"


class OneDriveCredentials(ConfiguredBaseModel):
    client_id: str
    secret: str
    tenant_id: str
    user_id: str


class SalesforceCredentials(ConfiguredBaseModel):
    client_id: str
    client_secret: str
    owner_id: str
    location_id: str


Credentials = Union[
    OneDriveCredentials,
    SalesforceCredentials,
]


class ExternalStorageInfo(ConfiguredBaseModel):
    code: ExternalStorageCode
