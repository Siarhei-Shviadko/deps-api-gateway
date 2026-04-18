import asyncio
from typing import Any, Optional, TypedDict, Union

from starlette.datastructures import UploadFile

from ..iproxies import (
    IAIFusionProxy,
    IEnrichmentProxy,
    IExtraction,
    IHighSparrowProxy,
    IOutputExportingProxy,
    IUnifierProxy,
    IWorkflowManagerProxy,
)
from ..parsing import (
    IParsingProxy,
    ISemanticParsingProxy,
    ParsingFeature,
    ParsingType,
    Provider,
)
from ..proxy_response import ProxyResponse
from ..types import (
    CellsReference,
    ElementType,
    InsightsRequestParamsDict,
    NeedsReviewOption,
    RawPoint,
    SaveExtraDataElement,
    Status,
)
from .consolidator import DocumentConsolidator
from .document_detail_extras import DocumentDetailExtras
from .document_proxy import IDocumentProxy
from .dtos import DocumentListFilterData, PartialUpdateDocumentData

__all__ = ["DocumentService"]


class _DocumentDetailResponse(TypedDict):
    document_detail_response: ProxyResponse


class _DocumentDetailResponses(_DocumentDetailResponse, total=False):
    output_exporting_response: ProxyResponse
    ai_fusion_response: ProxyResponse
    high_sparrow_response: ProxyResponse
    document_metadata_response: ProxyResponse
    parsing_response: ProxyResponse


class DocumentService:  # noqa: WPS214
    def __init__(
        self,
        document_proxy: IDocumentProxy,
        high_sparrow_proxy: IHighSparrowProxy,
        unifier_proxy: IUnifierProxy,
        parsing_proxy: IParsingProxy,
        semantic_parsing_proxy: ISemanticParsingProxy,
        output_exporting_proxy: IOutputExportingProxy,
        ai_fusion_proxy: IAIFusionProxy,
        workflow_manager_proxy: IWorkflowManagerProxy,
        extraction_proxy: IExtraction,
        enrichment_proxy: IEnrichmentProxy,
    ) -> None:
        self._document_proxy = document_proxy
        self._high_sparrow_proxy = high_sparrow_proxy
        self._unifier_proxy = unifier_proxy
        self._parsing_proxy = parsing_proxy
        self._semantic_parsing_proxy = semantic_parsing_proxy
        self._output_exporting_proxy = output_exporting_proxy
        self._ai_fusion_proxy = ai_fusion_proxy
        self._workflow_manager_proxy = workflow_manager_proxy
        self._extraction_proxy = extraction_proxy
        self._enrichment_proxy = enrichment_proxy

    async def get_document_list(self, filter_data: DocumentListFilterData) -> ProxyResponse:
        return await self._document_proxy.get_document_list(filter_data)

    async def get_document_detail(
        self,
        document_id: str,
        extras: Optional[list[DocumentDetailExtras]],
    ) -> ProxyResponse:
        result_dict: _DocumentDetailResponses = await self._gather_document_detail_requests(
            document_id=document_id,
            extras=extras,
        )

        return DocumentConsolidator.consolidate_document_detail(
            document_detail_response=result_dict["document_detail_response"],
            output_exporting_response=result_dict.get("output_exporting_response"),
            ai_fusion_response=result_dict.get("ai_fusion_response"),
            high_sparrow_response=result_dict.get("high_sparrow_response"),
            document_metadata_response=result_dict.get("document_metadata_response"),
            parsing_response=result_dict.get("parsing_response"),
        )

    async def partial_update_document(
        self, document_id: str, document_data: PartialUpdateDocumentData
    ) -> ProxyResponse:
        return await self._document_proxy.partial_update_document(document_id=document_id, document_data=document_data)

    async def delete_document_list(self, document_ids: list[str]) -> ProxyResponse:
        return DocumentConsolidator.consolidate_delete_document_list(
            await self._document_proxy.delete_document_list(document_ids)
        )

    async def add_comment(self, document_id: str, text: str) -> ProxyResponse:
        return await self._document_proxy.add_comment(document_id=document_id, text=text)

    async def get_labels(self) -> ProxyResponse:
        return DocumentConsolidator.consolidate_labels(await self._document_proxy.get_labels())

    async def remove_label_from_document(self, document_id: str, label_id: str) -> ProxyResponse:
        return DocumentConsolidator.consolidate_remove_label_response(
            await self._document_proxy.remove_label_from_document(document_id=document_id, label_id=label_id)
        )

    async def create_label(self, label_name: str) -> ProxyResponse:
        return await self._document_proxy.create_label(label_name)

    async def add_label_on_document(self, document_id: str, label_id: str) -> ProxyResponse:
        return DocumentConsolidator.consolidate_add_label_response(
            await self._document_proxy.add_label_on_document(document_id=document_id, label_id=label_id)
        )

    async def add_label_on_documents_batch(self, document_ids: list[str], label_id: str) -> ProxyResponse:
        return DocumentConsolidator.consolidate_add_label_batch_response(
            await self._document_proxy.add_label_on_documents_batch(document_ids=document_ids, label_id=label_id)
        )

    async def get_document_states(self) -> ProxyResponse:
        return DocumentConsolidator.consolidate_states(await self._document_proxy.get_document_states())

    async def get_validation_result(self, document_id: str) -> ProxyResponse:
        return await self._high_sparrow_proxy.get_validation_result(entity_id=document_id)

    async def get_unified_data(
        self,
        document_id: str,
        pos_text_blob_name: Optional[str] = None,
        unified_data_types: Optional[set[ElementType]] = None,
    ) -> ProxyResponse:
        return await self._unifier_proxy.get_unified_data(
            document_id=document_id, pos_text_blob_name=pos_text_blob_name, unified_data_types=unified_data_types
        )

    async def get_unified_cells_data(
        self,
        document_id: str,
        table_id: str,
        cells_reference: CellsReference,
    ) -> ProxyResponse:
        return await self._unifier_proxy.get_unified_cells_data(
            document_id=document_id,
            table_id=table_id,
            reference=cells_reference,
        )

    async def get_document_layout(
        self,
        document_id: str,
        parsing_type: ParsingType,
        features: Optional[set[ParsingFeature]] = None,
        batch_index: Optional[int] = None,
        batch_size: Optional[int] = None,
    ) -> ProxyResponse:
        return await self._parsing_proxy.get_document_layout(
            document_layout_id=document_id,
            parsing_type=parsing_type,
            features=features,
            batch_index=batch_index,
            batch_size=batch_size,
        )

    async def get_tabular_layout(
        self,
        document_id: str,
        tables: Optional[list[str]],
        row_span: Optional[tuple[int, int]],
        col_span: Optional[tuple[int, int]],
    ) -> ProxyResponse:
        return await self._parsing_proxy.get_tabular_layout(
            tabular_layout_id=document_id,
            tables=tables,
            row_span=row_span,
            col_span=col_span,
        )

    async def get_semantic_layout(
        self,
        layout_id: str,
        provider: Provider,
    ) -> ProxyResponse:
        return await self._semantic_parsing_proxy.get_semantic_layout(layout_id=layout_id, provider=provider)

    async def update_document_layout_image(
        self,
        document_id: str,
        page_id: str,
        image_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        filepath: Optional[str] = None,
        polygon: Optional[list[RawPoint]] = None,
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_document_layout_image(
            document_id=document_id,
            page_id=page_id,
            image_id=image_id,
            title=title,
            description=description,
            filepath=filepath,
            polygon=polygon,
        )

    async def get_outputs(self, document_id: str) -> ProxyResponse:
        return await self._output_exporting_proxy.get_outputs(document_id=document_id)

    async def build_output(self, document_id: str, document_type_id: str, profile_id: str) -> ProxyResponse:
        return await self._output_exporting_proxy.build_output(
            document_id=document_id,
            document_type_id=document_type_id,
            profile_id=profile_id,
        )

    async def delete_output(self, document_id: str, output_id: str) -> ProxyResponse:
        return await self._output_exporting_proxy.delete_output(document_id=document_id, output_id=output_id)

    async def create_completion(
        self,
        entity_id: str,
        provider: str,
        model: str,
        question: str,
        page_span: Optional[tuple[int, int]] = None,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.create_completion(
            entity_id=entity_id,
            provider=provider,
            model=model,
            question=question,
            page_span=page_span,
            files=files,
        )

    async def remove_completions(
        self,
        entity_id: str,
        completion_codes: list[str],
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.remove_completions(entity_id=entity_id, completion_codes=completion_codes)

    async def get_conversation(self, entity_id: str) -> ProxyResponse:
        return await self._ai_fusion_proxy.get_conversation(entity_id=entity_id)

    async def clear_conversation(self, entity_id: str) -> ProxyResponse:
        return await self._ai_fusion_proxy.clear_conversation(entity_id=entity_id)

    async def run_pipeline_from_step(
        self,
        document_ids: list[str],
        step: Status,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        llm_type: Optional[str] = None,
        parsing_features: Optional[set[ParsingFeature]] = None,
    ) -> ProxyResponse:
        return await self._workflow_manager_proxy.run_pipeline_from_step(
            document_ids=document_ids,
            step=step,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
        )

    async def get_document_metadata(self, document_id: str) -> ProxyResponse:
        return await self._document_proxy.get_document_metadata(document_id)

    async def download_original_files(self, document_id: str) -> ProxyResponse:
        return await self._document_proxy.download_original_files(document_id)

    async def download_preprocessed_files(self, document_id: str) -> ProxyResponse:
        return await self._document_proxy.download_preprocessed_files(document_id)

    async def get_extracted_data(self, document_id: str, rows_per_chunk: Optional[int]) -> ProxyResponse:
        return await self._extraction_proxy.get_extracted_data(document_id=document_id, rows_per_chunk=rows_per_chunk)

    async def get_document_supplement(self, document_id: str) -> ProxyResponse:
        return await self._enrichment_proxy.get_document_supplement(document_id)

    async def save_document_supplement(
        self,
        document_id: str,
        document_type_id: str,
        extra_data_list: list[SaveExtraDataElement],
    ) -> ProxyResponse:
        return await self._enrichment_proxy.save_document_supplement(
            document_id=document_id,
            document_type_id=document_type_id,
            extra_data_list=extra_data_list,
        )

    async def upload_document(
        self,
        document_name: str,
        file: UploadFile,
        document_type_id: Optional[str],
        engine: Optional[str],
        language: Optional[str],
        llm_type: Optional[str],
        parsing_features: list[str],
        needs_unifier: bool = True,
        needs_extraction: bool = True,
        assign_to_me: bool = False,
        metadata: Optional[dict[str, Any]] = None,
    ) -> ProxyResponse:
        return await self._workflow_manager_proxy.upload_document(
            document_name=document_name,
            file=file,
            document_type_id=document_type_id,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unifier=needs_unifier,
            needs_extraction=needs_extraction,
            assign_to_me=assign_to_me,
            metadata=metadata,
        )

    async def import_documents(
        self,
        paths: list[str],
        source: str,
        document_type_id: Optional[str],
        engine: Optional[str],
        language: Optional[str],
        llm_type: Optional[str],
        parsing_features: list[str],
        needs_unifier: bool = True,
        needs_extraction: bool = True,
        needs_parsing: Optional[bool] = None,
        needs_validation: Optional[bool] = None,
        needs_review: Optional[NeedsReviewOption] = None,
        needs_output_exporting: Optional[bool] = None,
        assign_to_me: bool = False,
    ) -> ProxyResponse:
        return await self._workflow_manager_proxy.import_documents(
            paths=paths,
            source=source,
            document_type_id=document_type_id,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unifier=needs_unifier,
            needs_extraction=needs_extraction,
            needs_parsing=needs_parsing,
            needs_validation=needs_validation,
            needs_review=needs_review,
            needs_output_exporting=needs_output_exporting,
            assign_to_me=assign_to_me,
        )

    async def validate_document(self, document_id: str) -> ProxyResponse:
        return await self._workflow_manager_proxy.validate_document(document_id=document_id)

    async def retry_last_failed_step(self, document_id: str) -> ProxyResponse:
        return await self._workflow_manager_proxy.retry_last_failed_step(document_id=document_id)

    async def run_from_first_step(self, document_id: str) -> ProxyResponse:
        return await self._workflow_manager_proxy.run_from_first_step(document_id=document_id)

    async def start_review(self, document_id: str) -> ProxyResponse:
        return await self._document_proxy.start_review(document_id=document_id)

    async def complete_review(self, document_id: str) -> ProxyResponse:
        return await self._workflow_manager_proxy.complete_review(document_id=document_id)

    async def assign_type(self, document_id: str, document_type_id: str) -> ProxyResponse:
        return DocumentConsolidator.consolidate_assigning_type(
            await self._document_proxy.assign_type(document_id=document_id, document_type_id=document_type_id)
        )

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
        return await self._document_proxy.create_document(
            document_name=document_name,
            file=file,
            document_type_id=document_type_id,
            group_id=group_id,
            engine=engine,
            language=language,
            llm_type=llm_type,
            parsing_features=parsing_features,
            needs_unification=needs_unification,
            needs_extraction=needs_extraction,
            needs_parsing=needs_parsing,
            needs_validation=needs_validation,
            needs_review=needs_review,
            needs_output_exporting=needs_output_exporting,
            assign_to_me=assign_to_me,
            metadata=metadata,
            label_ids=label_ids,
        )

    async def retrieve_insights(
        self,
        document_id: str,
        model: str,
        requested_insights: dict[str, Union[str, dict[str, Any]]],
        custom_instructions: Optional[str],
        params: InsightsRequestParamsDict,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.retrieve_insights(
            document_id=document_id,
            model=model,
            requested_insights=requested_insights,
            custom_instructions=custom_instructions,
            params=params,
            files=files,
        )

    async def retrieve_file_insights(
        self,
        filepath: str,
        model: str,
        requested_insights: dict[str, Union[str, dict[str, Any]]],
        custom_instructions: Optional[str],
        params: InsightsRequestParamsDict,
        files: Optional[list[str]] = None,
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.retrieve_file_insights(
            filepath=filepath,
            model=model,
            requested_insights=requested_insights,
            custom_instructions=custom_instructions,
            params=params,
            files=files,
        )

    async def update_paragraph(
        self,
        document_id: str,
        page_id: str,
        paragraph_id: str,
        update_paragraph_request: dict[str, Any],
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_paragraph(
            document_layout_id=document_id,
            page_id=page_id,
            paragraph_id=paragraph_id,
            update_paragraph_request=update_paragraph_request,
        )

    async def update_table(
        self,
        document_id: str,
        page_id: str,
        table_id: str,
        update_table_request: dict[str, Any],
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_table(
            document_layout_id=document_id,
            page_id=page_id,
            table_id=table_id,
            update_table_request=update_table_request,
        )

    async def update_key_value_pair(
        self,
        document_id: str,
        page_id: str,
        key_value_pair_id: str,
        update_key_value_pair_request: dict,
    ) -> ProxyResponse:
        return await self._parsing_proxy.update_key_value_pair(
            document_layout_id=document_id,
            page_id=page_id,
            key_value_pair_id=key_value_pair_id,
            update_key_value_pair_request=update_key_value_pair_request,
        )

    async def extract_data(self, document_ids: list[str], engine: str) -> ProxyResponse:
        return await self._document_proxy.extract_data(document_ids=document_ids, engine=engine)

    async def add_llm_coordinates(
        self,
        entity_id: str,
        field_codes: list[str],
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.add_llm_coordinates(
            entity_id=entity_id,
            field_codes=field_codes,
        )

    async def _gather_document_detail_requests(
        self, document_id: str, extras: Optional[list[DocumentDetailExtras]]
    ) -> _DocumentDetailResponses:
        coroutines = {"document_detail_response": self._document_proxy.get_document_detail(document_id)}

        if extras is not None:
            if DocumentDetailExtras.OUTPUTS in extras:
                coroutines["output_exporting_response"] = self._output_exporting_proxy.get_outputs(document_id)
            if DocumentDetailExtras.CONVERSATION in extras:
                coroutines["ai_fusion_response"] = self._ai_fusion_proxy.get_conversation(document_id)
            if DocumentDetailExtras.VALIDATION_RESULTS in extras:
                coroutines["high_sparrow_response"] = self._high_sparrow_proxy.get_validation_result(document_id)
            if DocumentDetailExtras.METADATA in extras:
                coroutines["document_metadata_response"] = self._document_proxy.get_document_metadata(document_id)
            if DocumentDetailExtras.PARSING_INFO in extras:
                coroutines["parsing_response"] = self._parsing_proxy.get_parsing_info(document_id)

        return _DocumentDetailResponses(
            zip(coroutines.keys(), await asyncio.gather(*coroutines.values()))  # type: ignore
        )
