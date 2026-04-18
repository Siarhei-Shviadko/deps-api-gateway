from pathlib import PurePosixPath
from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application import (
    IStorageProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import STORAGE_BASE_API_PREFIX, V1_PREFIX

from ..form_data import FormDataBuilder
from ..generic_rest_client import GenericRestClient
from .exceptions import StorageError, StorageServiceUnavailableError

__all__ = ["StorageProxy"]


class StorageProxy(GenericRestClient, IStorageProxy):
    exception = StorageError
    url_prefix = f"{STORAGE_BASE_API_PREFIX}{V1_PREFIX}/file"
    FILE_FIELD_NAME: str = "file"

    async def download_file(
        self,
        path: str,
        storage: str,
    ) -> ProxyResponse:
        url = f"{self.url_prefix}/{path}"

        data: dict[str, Any] = {
            "storage": storage,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=url,
                    params=data,
                )
            )

    async def upload_file(
        self,
        directory_path: str,
        file_name: str,
        content: bytes,
        replace_if_exists: bool,
        storage_name: str,
    ) -> ProxyResponse:
        url = f"{self.url_prefix}/{PurePosixPath(directory_path)}" if directory_path else self.url_prefix
        form_data = (
            FormDataBuilder()
            .with_file(field_name=self.FILE_FIELD_NAME, filename=file_name, content=content)
            .with_field(key="storage", value=storage_name)
            .with_field(key="replaceIfExists", value=str(replace_if_exists))
            .build()
        )

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data.data, headers=form_data.headers),
            )

        except Exception as error:
            raise StorageServiceUnavailableError(error)

    async def delete_file(
        self,
        path: str,
        storage: str,
    ) -> ProxyResponse:
        url = f"{self.url_prefix}/{path}"

        data: dict[str, Any] = {
            "storage": storage,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=url,
                    params=data,
                )
            )
