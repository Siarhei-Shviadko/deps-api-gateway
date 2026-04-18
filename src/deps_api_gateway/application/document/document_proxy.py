from typing import Any, Optional, Protocol

from fastapi import UploadFile

from ..proxy_response import ProxyResponse
from ..types.workflow_manager import NeedsReviewOption
from .dtos import DocumentListFilterData, PartialUpdateDocumentData

__all__ = ["IDocumentProxy"]


class IDocumentProxy(Protocol):
    async def get_document_list(self, filter_data: DocumentListFilterData) -> ProxyResponse:
        ...

    async def get_document_detail(self, document_id: str) -> ProxyResponse:
        ...

    async def partial_update_document(
        self, document_id: str, document_data: PartialUpdateDocumentData
    ) -> ProxyResponse:
        ...

    async def delete_document_list(self, document_ids: list[str]) -> ProxyResponse:
        ...

    async def add_comment(self, document_id: str, text: str) -> ProxyResponse:
        ...

    async def get_labels(self) -> ProxyResponse:
        ...

    async def remove_label_from_document(self, document_id: str, label_id: str) -> ProxyResponse:
        ...

    async def create_label(self, label_name: str) -> ProxyResponse:
        ...

    async def add_label_on_document(self, document_id: str, label_id: str) -> ProxyResponse:
        ...

    async def add_label_on_documents_batch(self, document_ids: list[str], label_id: str) -> ProxyResponse:
        ...

    async def get_document_states(self) -> ProxyResponse:
        ...

    async def get_document_metadata(self, document_id: str) -> ProxyResponse:
        ...

    async def download_original_files(self, document_id: str) -> ProxyResponse:
        ...

    async def download_preprocessed_files(self, document_id: str) -> ProxyResponse:
        ...

    async def start_review(self, document_id: str) -> ProxyResponse:
        ...

    async def assign_type(self, document_id: str, document_type_id: str) -> ProxyResponse:
        ...

    async def create_document(
        self,
        document_name: str,
        file: UploadFile,
        document_type_id: Optional[str] = None,
        group_id: Optional[str] = None,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        llm_type: Optional[str] = None,
        parsing_features: Optional[list[str]] = None,
        needs_unification: bool = True,
        needs_extraction: bool = True,
        needs_parsing: Optional[bool] = None,
        needs_validation: Optional[bool] = None,
        needs_review: Optional[NeedsReviewOption] = None,
        needs_output_exporting: Optional[bool] = None,
        assign_to_me: bool = False,
        metadata: Optional[dict[str, Any]] = None,
        label_ids: Optional[list[str]] = None,
    ) -> ProxyResponse:
        ...

    async def extract_data(self, document_ids: list[str], engine: str) -> ProxyResponse:
        ...
