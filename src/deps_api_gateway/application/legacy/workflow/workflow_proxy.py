from typing import Any, Optional, Protocol

from async_rest_client import Methods
from starlette.datastructures import UploadFile

__all__ = ["IWorkflow"]


class IWorkflow(Protocol):
    async def upload_document(
        self,
        url: str,
        form: dict[str, Any],
        file: Optional[UploadFile],
        headers: dict[str, Any],
    ) -> dict:
        ...

    async def upload_document_v2(self, form: dict[str, Any], headers: dict[str, Any]) -> dict:
        ...

    async def import_documents(
        self,
        url: str,
        body: dict[str, Any],
        headers: dict[str, Any],
    ) -> None:
        ...

    async def get_saga_state(self, url: str, query: str, headers: dict[str, Any]) -> str:
        ...

    async def request(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        ...
