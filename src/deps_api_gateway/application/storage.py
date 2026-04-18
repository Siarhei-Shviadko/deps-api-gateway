from pathlib import Path
from uuid import uuid4

from .iproxies import IStorageProxy
from .proxy_response import ProxyResponse

__all__ = ["StorageService"]


class StorageService:
    def __init__(self, proxy: IStorageProxy) -> None:
        self._proxy = proxy

    async def download_file(self, path: str, storage: str) -> ProxyResponse:
        return await self._proxy.download_file(
            path=path,
            storage=storage,
        )

    async def upload_file_with_unique_path(self, file_name: str, content: bytes, storage_name: str) -> ProxyResponse:
        extension = Path(file_name).suffix

        return await self._proxy.upload_file(
            directory_path="",
            file_name=f"{uuid4().hex}{extension}",
            content=content,
            replace_if_exists=False,
            storage_name=storage_name,
        )

    async def delete_file(self, path: str, storage: str) -> ProxyResponse:
        return await self._proxy.delete_file(
            path=path,
            storage=storage,
        )
