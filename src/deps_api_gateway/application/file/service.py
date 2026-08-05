from datetime import datetime
from typing import Any

from fastapi import UploadFile

from ..iproxies import IUnifierProxy
from ..parsing import IParsingProxy, ParsingFeature, ParsingType
from ..proxy_response import ProxyResponse
from ..types import CellsReference, ElementType, RawPoint
from .file_proxy import IFileProxy

__all__ = ["FileService"]


class FileService:
    def __init__(
        self,
        file_proxy: IFileProxy,
        unifier_proxy: IUnifierProxy,
        parsing_proxy: IParsingProxy,
    ) -> None:
        self._file_proxy = file_proxy
        self._unifier_proxy = unifier_proxy
        self._parsing_proxy = parsing_proxy

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
        return await self._file_proxy.get_files(
            name=name,
            state=state,
            labels=labels,
            date_start=date_start,
            date_end=date_end,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            reference_available=reference_available,
            reference=reference,
        )

    async def get_file(self, file_id: str) -> ProxyResponse:
        return await self._file_proxy.get_file(file_id)

    async def get_unified_data(
        self,
        file_id: str,
        pos_text_blob_name: str | None = None,
        unified_data_types: set[ElementType] | None = None,
    ) -> ProxyResponse:
        return await self._unifier_proxy.get_unified_data(
            document_id=file_id,
            pos_text_blob_name=pos_text_blob_name,
            unified_data_types=unified_data_types,
        )

    async def get_unified_cells_data(
        self,
        file_id: str,
        table_id: str,
        cells_reference: CellsReference,
    ) -> ProxyResponse:
        return await self._unifier_proxy.get_unified_cells_data(
            document_id=file_id,
            table_id=table_id,
            reference=cells_reference,
        )

    async def get_parsing_info(self, file_id: str) -> ProxyResponse:
        return await self._parsing_proxy.get_parsing_info(file_id)

    async def get_file_layout(
        self,
        file_id: str,
        parsing_type: ParsingType,
        features: set[ParsingFeature] | None = None,
        batch_index: int | None = None,
        batch_size: int | None = None,
    ) -> ProxyResponse:
        return await self._parsing_proxy.get_document_layout(
            document_layout_id=file_id,
            parsing_type=parsing_type,
            features=features,
            batch_index=batch_index,
            batch_size=batch_size,
        )

    async def get_tabular_layout(
        self,
        file_id: str,
        tables: list[str] | None = None,
        row_span: tuple[int, int] | None = None,
        col_span: tuple[int, int] | None = None,
    ) -> ProxyResponse:
        return await self._parsing_proxy.get_tabular_layout(
            tabular_layout_id=file_id,
            tables=tables,
            row_span=row_span,
            col_span=col_span,
        )

    async def clone_document_layout(self, file_id: str, parsing_type: str) -> ProxyResponse:
        return await self._parsing_proxy.clone_document_layout(document_id=file_id, parsing_type=parsing_type)

    async def update_paragraph(
        self,
        file_id: str,
        page_id: str,
        paragraph_id: str,
        update_paragraph_request: dict[str, Any],
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_paragraph(
            document_layout_id=file_id,
            page_id=page_id,
            paragraph_id=paragraph_id,
            update_paragraph_request=update_paragraph_request,
        )

    async def update_document_layout_image(
        self,
        file_id: str,
        page_id: str,
        image_id: str,
        title: str | None = None,
        description: str | None = None,
        filepath: str | None = None,
        polygon: list[RawPoint] | None = None,
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_document_layout_image(
            document_id=file_id,
            page_id=page_id,
            image_id=image_id,
            title=title,
            description=description,
            filepath=filepath,
            polygon=polygon,
        )

    async def update_table(
        self,
        file_id: str,
        page_id: str,
        table_id: str,
        update_table_request: dict[str, Any],
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_table(
            document_layout_id=file_id,
            page_id=page_id,
            table_id=table_id,
            update_table_request=update_table_request,
        )

    async def update_key_value_pair(
        self,
        file_id: str,
        page_id: str,
        key_value_pair_id: str,
        update_key_value_pair_request: dict,
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_key_value_pair(
            document_layout_id=file_id,
            page_id=page_id,
            key_value_pair_id=key_value_pair_id,
            update_key_value_pair_request=update_key_value_pair_request,
        )

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
        metadata: dict[str, Any] | None,
    ) -> ProxyResponse:
        return await self._file_proxy.process_file(
            file=file,
            labels=labels,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unifier=needs_unifier,
            needs_extraction=needs_extraction,
            assigned_to_me=assigned_to_me,
            metadata=metadata,
        )

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
        metadata: dict[str, Any] | None,
    ) -> ProxyResponse:
        return await self._file_proxy.classify_file(
            file=file,
            group_id=group_id,
            labels=labels,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unifier=needs_unifier,
            needs_extraction=needs_extraction,
            assigned_to_me=assigned_to_me,
            metadata=metadata,
        )

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
        metadata: dict[str, Any] | None,
    ) -> ProxyResponse:
        return await self._file_proxy.classify_existing_file(
            file_id=file_id,
            group_id=group_id,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unifier=needs_unifier,
            needs_extraction=needs_extraction,
            assigned_to_me=assigned_to_me,
            metadata=metadata,
        )

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
        needs_splitting_proposal_review: bool,
        metadata: dict[str, Any] | None,
    ) -> ProxyResponse:
        return await self._file_proxy.split_file(
            file=file,
            document_type_id=document_type_id,
            classification_enabled=classification_enabled,
            group_id=group_id,
            labels=labels,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unifier=needs_unifier,
            needs_extraction=needs_extraction,
            assigned_to_me=assigned_to_me,
            needs_splitting_proposal_review=needs_splitting_proposal_review,
            metadata=metadata,
        )

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
        needs_splitting_proposal_review: bool,
        metadata: dict[str, Any] | None,
    ) -> ProxyResponse:
        return await self._file_proxy.split_existing_file(
            file_id=file_id,
            document_type_id=document_type_id,
            classification_enabled=classification_enabled,
            group_id=group_id,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unifier=needs_unifier,
            needs_extraction=needs_extraction,
            assigned_to_me=assigned_to_me,
            needs_splitting_proposal_review=needs_splitting_proposal_review,
            metadata=metadata,
        )

    async def delete_files(self, ids: list[str]) -> ProxyResponse:
        return await self._file_proxy.delete_files(ids)

    async def create_document_from_file(
        self,
        file_id: str,
        document_type_id: str,
    ) -> ProxyResponse:
        return await self._file_proxy.create_document_from_file(
            file_id=file_id,
            document_type_id=document_type_id,
        )

    async def create_batch_from_file(
        self,
        file_id: str,
        batch_name: str,
        batch_files: list[dict[str, Any]],
        group_id: str | None,
    ) -> ProxyResponse:
        return await self._file_proxy.create_batch_from_file(
            file_id=file_id,
            batch_name=batch_name,
            batch_files=batch_files,
            group_id=group_id,
        )

    async def restart_file(self, file_id: str) -> ProxyResponse:
        return await self._file_proxy.restart_file(file_id=file_id)
