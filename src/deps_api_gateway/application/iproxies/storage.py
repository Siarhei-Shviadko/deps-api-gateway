from typing import Protocol

from ..proxy_response import ProxyResponse

__all__ = ["IStorageProxy"]


class IStorageProxy(Protocol):
    async def download_file(
        self,
        path: str,
        storage: str,
    ) -> ProxyResponse:
        pass

    async def upload_file(
        self,
        directory_path: str,
        file_name: str,
        content: bytes,
        replace_if_exists: bool,
        storage_name: str,
    ) -> ProxyResponse:
        pass

    async def delete_file(
        self,
        path: str,
        storage: str,
    ) -> ProxyResponse:
        pass
