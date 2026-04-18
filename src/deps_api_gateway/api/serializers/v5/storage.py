from ..base import ConfiguredBaseModel

__all__ = ["DownloadFileResponse", "UploadFileResponse"]


class DownloadFileResponse(ConfiguredBaseModel):
    file: bytes


class UploadFileResponse(ConfiguredBaseModel):
    path: str
