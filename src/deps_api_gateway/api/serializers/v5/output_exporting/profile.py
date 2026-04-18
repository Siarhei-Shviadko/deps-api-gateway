from datetime import date
from typing import Optional, Union

from pydantic import Field

from ...base import ConfiguredBaseModel
from .external_storage_info import Credentials, ExternalStorageCode, ExternalStorageInfo
from .format import Format
from .schemas import DocumentLayoutSchema, ExtractedDataSchema

__all__ = ["SerializedOutputProfile", "CreateProfileRequest", "SaveProfileResponse", "UpdateProfileRequest"]


class CreateExternalStorageInfo(ConfiguredBaseModel):
    code: ExternalStorageCode
    credentials: Credentials
    output_directory_path: Optional[str] = None


class SerializedOutputProfile(ConfiguredBaseModel):
    id: str
    name: str
    creation_date: date
    schema_: Union[ExtractedDataSchema, DocumentLayoutSchema] = Field(  # noqa: WPS120
        alias="schema",
    )
    version: str
    format: Format
    external_storages_info: Optional[list[ExternalStorageInfo]]


class CreateProfileRequest(ConfiguredBaseModel):
    name: str
    schema_: Union[ExtractedDataSchema, DocumentLayoutSchema] = Field(  # noqa: WPS120
        alias="schema",
    )
    format: Format
    external_storages_info: Optional[list[CreateExternalStorageInfo]] = None


class SaveProfileResponse(ConfiguredBaseModel):
    id: str


class UpdateProfileRequest(ConfiguredBaseModel):
    name: str
    schema_: Union[ExtractedDataSchema, DocumentLayoutSchema] = Field(  # noqa: WPS120
        alias="schema",
    )
    external_storages_info: Optional[list[CreateExternalStorageInfo]] = None
