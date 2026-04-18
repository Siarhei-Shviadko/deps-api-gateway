from datetime import datetime
from typing import Any, Protocol

from fastapi import UploadFile

from deps_api_gateway.application.proxy_response import ProxyResponse

__all__ = ["IFileProxy"]


class IFileProxy(Protocol):
    async def get_files(
        self,
        name: str | None,
        state: list[str] | None,
        labels: list[str] | None,
        date_start: datetime | None,
        date_end: datetime | None,
        page: int | None,
        per_page: int | None,
        sort_by: str,
        sort_order: str,
        reference_available: bool | None,
        reference: str | None,
    ) -> ProxyResponse:
        pass

    async def get_file(self, file_id: str) -> ProxyResponse:
        pass

    async def process_file(
        self,
        file: UploadFile,
        labels: list[str] | None,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        pass

    async def classify_file(
        self,
        file: UploadFile,
        group_id: str,
        labels: list[str] | None,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        pass

    async def classify_existing_file(
        self,
        file_id: str,
        group_id: str,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        pass

    async def split_file(
        self,
        file: UploadFile,
        document_type_id: str | None,
        classification_enabled: bool,
        group_id: str,
        labels: list[str] | None,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        pass

    async def split_existing_file(
        self,
        file_id: str,
        document_type_id: str | None,
        classification_enabled: bool,
        group_id: str,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        pass

    async def delete_files(self, ids: list[str]) -> ProxyResponse:
        pass

    async def create_document_from_file(
        self,
        file_id: str,
        document_type_id: str,
    ) -> ProxyResponse:
        pass

    async def create_batch_from_file(
        self,
        file_id: str,
        batch_name: str,
        batch_files: list[dict[str, Any]],
        group_id: str | None,
    ) -> ProxyResponse:
        pass

    async def restart_file(self, file_id: str) -> ProxyResponse:
        pass
