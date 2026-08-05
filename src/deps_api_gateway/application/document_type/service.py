import asyncio
from typing import Any, Optional, TypedDict

from starlette.datastructures import UploadFile

from deps_api_gateway.domain import ExtractionFieldData, ExtraFieldData, ProfileData

from ...constants import ExtractionType
from ..iproxies import (
    IAIFusionProxy,
    IClassificationProxy,
    ICloudNativeExtractionProxy,
    IEnrichmentProxy,
    IExtraction,
    IHighSparrowProxy,
    IOutputExportingProxy,
    IUnifierProxy,
    IWorkflowManagerProxy,
)
from ..parsing import IParsingProxy
from ..proxy_response import ProxyResponse
from ..types import ExtractorType, FieldType, RawDataShape, RawLLMWorkflow, Severity
from .consolidator import DocumentTypeConsolidator
from .document_type_proxy import IDocumentTypeProxy
from .exceptions import ExtractorAttachmentError
from .inclusion_params import DocumentTypeExtras
from .prototype import (
    GetPrototypeExtras,
    Header,
    HeaderType,
    IPrototypeProxy,
    MappingType,
    PrototypeConsolidator,
    PrototypeDataTypeCode,
)
from .template import ITemplateProxy, TemplateConsolidator, TemplateDataTypeCode

__all__ = ["DocumentTypeService"]


class _RequiredDocumentTypeResponses(TypedDict):
    document_type_response: ProxyResponse


class _DocumentTypeResponses(_RequiredDocumentTypeResponses, total=False):
    extraction_response: ProxyResponse
    enrichment_response: ProxyResponse
    high_sparrow_response: ProxyResponse
    output_exporting_response: ProxyResponse
    classification_response: ProxyResponse
    ai_fusion_response: ProxyResponse
    workflow_manager_response: ProxyResponse


class _DocumentTypesResponses(TypedDict):
    document_types_response: ProxyResponse
    workflow_configurations_response: ProxyResponse


class _RequiredGetPrototypeResponses(TypedDict):
    prototype_response: ProxyResponse
    extraction_response: ProxyResponse


class _GetPrototypeResponses(_RequiredGetPrototypeResponses, total=False):
    layouts_response: ProxyResponse


class _GetReferenceLayoutResponses(TypedDict):
    reference_layouts_response: ProxyResponse
    unified_data_response: ProxyResponse
    document_layout_data_response: ProxyResponse


class DocumentTypeService:
    def __init__(
        self,
        high_sparrow_proxy: IHighSparrowProxy,
        extraction_proxy: IExtraction,
        prototype_proxy: IPrototypeProxy,
        document_type_proxy: IDocumentTypeProxy,
        output_exporting_proxy: IOutputExportingProxy,
        enrichment_proxy: IEnrichmentProxy,
        template_proxy: ITemplateProxy,
        workflow_manager_proxy: IWorkflowManagerProxy,
        cloud_native_extraction_proxy: ICloudNativeExtractionProxy,
        classification_proxy: IClassificationProxy,
        ai_fusion_proxy: IAIFusionProxy,
        unifier_proxy: IUnifierProxy,
        parsing_proxy: IParsingProxy,
    ) -> None:
        self._high_sparrow_proxy = high_sparrow_proxy
        self._extraction_proxy = extraction_proxy
        self._prototype_proxy = prototype_proxy
        self._document_type_proxy = document_type_proxy
        self._output_exporting_proxy = output_exporting_proxy
        self._enrichment_proxy = enrichment_proxy
        self._template_proxy = template_proxy
        self._workflow_manager_proxy = workflow_manager_proxy
        self._cloud_native_extraction_proxy = cloud_native_extraction_proxy
        self._classification_proxy = classification_proxy
        self._ai_fusion_proxy = ai_fusion_proxy
        self._unifier_proxy = unifier_proxy
        self._parsing_proxy = parsing_proxy

    async def get_document_types(
        self, extraction_type: Optional[ExtractionType] = None, workflow_configurations: Optional[bool] = False
    ) -> ProxyResponse:
        tasks = {
            "document_types_response": self._document_type_proxy.get_document_types(extraction_type=extraction_type)
        }
        if workflow_configurations:
            tasks["workflow_configurations_response"] = self._workflow_manager_proxy.get_workflow_configurations()

        result_dict: _DocumentTypesResponses = _DocumentTypesResponses(
            zip(tasks.keys(), await asyncio.gather(*tasks.values()))  # type: ignore
        )

        return DocumentTypeConsolidator.consolidate_document_types(
            document_types_response=result_dict["document_types_response"],
            workflow_configurations_response=result_dict.get("workflow_configurations_response", None),
        )

    async def get_document_type(
        self,
        document_type_id: str,
        extras: Optional[list[DocumentTypeExtras]] = None,
    ) -> ProxyResponse:
        result_dict: _DocumentTypeResponses = await self._gather_document_type_requests(
            document_type_id=document_type_id,
            extras=extras,
        )

        return DocumentTypeConsolidator.consolidate_document_type(
            document_type_response=result_dict["document_type_response"],
            extraction_response=result_dict.get("extraction_response", None),
            enrichment_response=result_dict.get("enrichment_response", None),
            high_sparrow_response=result_dict.get("high_sparrow_response", None),
            output_exporting_response=result_dict.get("output_exporting_response", None),
            classification_response=result_dict.get("classification_response", None),
            ai_fusion_response=result_dict.get("ai_fusion_response", None),
            workflow_manager_response=result_dict.get("workflow_manager_response", None),
            extras=extras,
        )

    async def delete_document_type(self, document_type_id: str) -> ProxyResponse:
        return await self._document_type_proxy.delete_document_type(document_type_id)

    async def update_document_type_llm(self, document_type_id: str, llm_type: str) -> ProxyResponse:
        return await self._document_type_proxy.update_document_type_llm(
            document_type_id=document_type_id,
            llm_type=llm_type,
        )

    async def attach_validator(
        self,
        document_type_id: str,
        external_validator_name: str,
        external_validator_url: str,
    ) -> ProxyResponse:
        return await self._high_sparrow_proxy.attach_validator(
            document_type_id=document_type_id,
            external_validator_name=external_validator_name,
            external_validator_url=external_validator_url,
        )

    async def remove_validator(
        self,
        document_type_id: str,
        external_validator_name: str,
    ) -> ProxyResponse:
        return await self._high_sparrow_proxy.remove_validator(
            document_type_id=document_type_id,
            external_validator_name=external_validator_name,
        )

    async def create_rule(
        self,
        document_type_id: str,
        validator_code: str,
        name: str,
        severity: Severity,
        rule: str,
        issue_message: str,
        description: str,
        need_warning_even_if_optional: bool,
        for_each: bool,
        for_any: bool,
        check_optional_fields: bool,
    ) -> ProxyResponse:
        return await self._high_sparrow_proxy.create_rule(
            document_type_id=document_type_id,
            validator_code=validator_code,
            name=name,
            severity=severity,
            rule=rule,
            issue_message=issue_message,
            description=description,
            need_warning_even_if_optional=need_warning_even_if_optional,
            for_each=for_each,
            for_any=for_any,
            check_optional_fields=check_optional_fields,
        )

    async def attach_cross_field_validator(
        self,
        document_type_id: str,
        name: str,
        description: str,
        rule: str,
        severity: Severity,
        validated_fields: list[str],
        issue_message: str,
        dependent_fields: list[str],
        for_each: bool = False,
        for_any: bool = False,
    ) -> ProxyResponse:
        return await self._high_sparrow_proxy.attach_cross_field_validator(
            document_type_id=document_type_id,
            name=name,
            description=description,
            rule=rule,
            severity=severity,
            validated_fields=validated_fields,
            issue_message=issue_message,
            dependent_fields=dependent_fields,
            for_each=for_each,
            for_any=for_any,
        )

    async def update_cross_field_validator(
        self,
        validator_id: str,
        document_type_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        rule: Optional[str] = None,
        severity: Optional[Severity] = None,
        validated_fields: Optional[list[str]] = None,
        issue_message: Optional[str] = None,
        dependent_fields: Optional[list[str]] = None,
        for_each: Optional[bool] = None,
        for_any: Optional[bool] = None,
    ) -> ProxyResponse:
        return await self._high_sparrow_proxy.update_cross_field_validator(
            validator_id=validator_id,
            document_type_id=document_type_id,
            name=name,
            description=description,
            rule=rule,
            severity=severity,
            validated_fields=validated_fields,
            issue_message=issue_message,
            dependent_fields=dependent_fields,
            for_each=for_each,
            for_any=for_any,
        )

    async def delete_cross_field_validator(self, document_type_id: str, validator_id: str) -> ProxyResponse:
        return await self._high_sparrow_proxy.delete_cross_field_validator(
            document_type_id=document_type_id,
            validator_id=validator_id,
        )

    async def delete_rule(
        self,
        document_type_id: str,
        validator_code: str,
        rule_name: str,
    ) -> ProxyResponse:
        return await self._high_sparrow_proxy.delete_rule(
            document_type_id=document_type_id, validator_code=validator_code, rule_name=rule_name
        )

    async def create_field(
        self,
        document_type_id: str,
        name: str,
        field_type: FieldType,
        description: Optional[dict[str, Any]],
        required: bool,
        confidential: bool,
        read_only: bool,
        order: int,
        extractor_id: Optional[str],
        field_code: Optional[str],
    ) -> ProxyResponse:
        return await self._extraction_proxy.create_field(
            document_type_id=document_type_id,
            name=name,
            field_type=field_type,
            description=description,
            required=required,
            confidential=confidential,
            read_only=read_only,
            order=order,
            extractor_id=extractor_id,
            field_code=field_code,
        )

    async def update_field(
        self,
        document_type_id: str,
        field_code: str,
        name: Optional[str],
        description: Optional[dict[str, Any]],
        required: Optional[bool],
        confidential: Optional[bool],
        read_only: Optional[bool],
        order: Optional[int],
        extractor_id: Optional[str],
    ) -> ProxyResponse:
        return await self._extraction_proxy.update_field(
            document_type_id=document_type_id,
            field_code=field_code,
            name=name,
            description=description,
            required=required,
            confidential=confidential,
            read_only=read_only,
            order=order,
            extractor_id=extractor_id,
        )

    async def update_fields(
        self,
        document_type_id: str,
        fields: list[ExtractionFieldData],
    ) -> ProxyResponse:
        return await self._extraction_proxy.update_fields(document_type_id=document_type_id, fields=fields)

    async def delete_fields(self, document_type_id: str, field_codes: list[str]) -> ProxyResponse:
        return await self._extraction_proxy.delete_fields(
            document_type_id=document_type_id,
            field_codes=field_codes,
        )

    async def create_mapping(
        self,
        document_type_id: str,
        code: str,
        data_type: PrototypeDataTypeCode,
        keys: list[str],
        mapping_type: MappingType,
    ) -> ProxyResponse:
        return await self._prototype_proxy.create_mapping(
            document_type_id=document_type_id,
            code=code,
            data_type=data_type,
            keys=keys,
            mapping_type=mapping_type,
        )

    async def update_mapping(
        self,
        document_type_id: str,
        code: str,
        keys: list[str],
    ) -> ProxyResponse:
        return await self._prototype_proxy.update_mapping(
            document_type_id=document_type_id,
            code=code,
            keys=keys,
        )

    async def create_tabular_mapping(
        self,
        code: str,
        document_type_id: str,
        header_type: HeaderType,
        headers: list[Header],
        occurrence_index: int,
    ) -> ProxyResponse:
        return await self._prototype_proxy.create_tabular_mapping(
            code=code,
            document_type_id=document_type_id,
            header_type=header_type,
            headers=headers,
            occurrence_index=occurrence_index,
        )

    async def update_tabular_mapping(
        self,
        document_type_id: str,
        code: str,
        header_type: Optional[HeaderType],
        headers: Optional[list[Header]],
        occurrence_index: Optional[int],
    ) -> ProxyResponse:
        return await self._prototype_proxy.update_tabular_mapping(
            document_type_id=document_type_id,
            code=code,
            header_type=header_type,
            headers=headers,
            occurrence_index=occurrence_index,
        )

    async def get_prototype(
        self,
        document_type_id: str,
        extras: Optional[list[GetPrototypeExtras]],
    ) -> ProxyResponse:
        result_dict: _GetPrototypeResponses = await self._gather_get_prototype_requests(
            document_type_id=document_type_id,
            extras=extras,
        )

        return PrototypeConsolidator.consolidate_prototype(
            extraction_response=result_dict["extraction_response"],
            prototype_response=result_dict["prototype_response"],
            layouts_response=result_dict.get("layouts_response", None),
        )

    async def create_prototype(
        self,
        name: str,
        engine: str,
        language: str,
        description: Optional[str],
    ) -> ProxyResponse:
        return await self._prototype_proxy.create_prototype(
            name=name,
            engine=engine,
            language=language,
            description=description,
        )

    async def update_prototype(
        self,
        document_type_id: str,
        engine: Optional[str],
        language: Optional[str],
        description: Optional[str],
    ) -> ProxyResponse:
        return await self._prototype_proxy.update_prototype(
            document_type_id=document_type_id,
            engine=engine,
            language=language,
            description=description,
        )

    async def get_reference_layouts(self, document_type_id: str) -> ProxyResponse:
        return await self._prototype_proxy.get_reference_layouts(document_type_id)

    async def get_reference_layout(self, document_type_id: str, layout_id: str) -> ProxyResponse:
        result_dict: _GetReferenceLayoutResponses = await self._gather_get_reference_layout_requests(
            document_type_id=document_type_id,
            layout_id=layout_id,
        )

        return PrototypeConsolidator.consolidate_reference_layout(
            reference_layout_response=result_dict["reference_layouts_response"],
            unified_data_response=result_dict["unified_data_response"]
            if result_dict["unified_data_response"].is_ok()
            else None,
            document_layout_data_response=result_dict["document_layout_data_response"]
            if result_dict["document_layout_data_response"].is_ok()
            else None,
        )

    async def create_reference_layout(self, document_type_id: str, file: UploadFile) -> ProxyResponse:
        return await self._prototype_proxy.create_reference_layout(document_type_id=document_type_id, file=file)

    async def delete_reference_layouts(self, document_type_id: str, layout_ids: list[str]) -> ProxyResponse:
        return await self._prototype_proxy.delete_reference_layouts(
            document_type_id=document_type_id,
            layout_ids=layout_ids,
        )

    async def restart_reference_layout(self, document_type_id: str, layout_id: str) -> ProxyResponse:
        return await self._prototype_proxy.restart_reference_layout(
            document_type_id=document_type_id,
            layout_id=layout_id,
        )

    async def attach_extractor(
        self,
        name: str,
        extractor_type: ExtractorType,
        fields: list[dict[str, Any]],
        description: Optional[str] = None,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        image_transformations: Optional[list[str]] = None,
    ) -> ProxyResponse:
        if extractor_type not in {ExtractorType.NON, ExtractorType.PLUGIN}:
            raise ExtractorAttachmentError("Can't attach Template or Prototype Extractors")

        return await self._extraction_proxy.attach_extractor(
            name=name,
            extractor_type=extractor_type,
            fields=fields,
            description=description,
            engine=engine,
            language=language,
            image_transformations=image_transformations,
        )

    async def create_template(
        self,
        src_template_id: Optional[str],
        name: str,
        language: str,
        engine: str,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> ProxyResponse:
        if src_template_id is None:
            return await self._workflow_manager_proxy.create_template(
                name=name,
                language=language,
                engine=engine,
                description=description,
                group_id=group_id,
            )

        return await self._workflow_manager_proxy.create_template_from(
            src_template_id=src_template_id,
            name=name,
            language=language,
            engine=engine,
            description=description,
            group_id=group_id,
        )

    async def get_template_versions(self, document_type_id: str) -> ProxyResponse:
        return TemplateConsolidator.consolidate_template_versions(
            await self._template_proxy.get_template_versions(document_type_id)
        )

    async def get_template_version(self, document_type_id: str, version_id: str) -> ProxyResponse:
        return await self._template_proxy.get_template_version(document_type_id=document_type_id, version_id=version_id)

    async def create_template_version(
        self,
        document_type_id: str,
        files: list[UploadFile],
        name: str,
        description: Optional[str] = None,
        markup_automatically: bool = False,
    ) -> ProxyResponse:
        return await self._workflow_manager_proxy.create_template_version(
            document_type_id=document_type_id,
            files=files,
            name=name,
            description=description,
            markup_automatically=markup_automatically,
        )

    async def update_template_version(self, document_type_id: str, version_id: str, name: str) -> ProxyResponse:
        return await self._template_proxy.update_template_version(
            document_type_id=document_type_id, version_id=version_id, name=name
        )

    async def add_markup(
        self,
        document_type_id: str,
        version_id: str,
        reference_page: str,
        markups: dict[str, list[list[float]]],
        markup_types: dict[str, TemplateDataTypeCode],
    ) -> ProxyResponse:
        return await self._template_proxy.add_markup(
            document_type_id=document_type_id,
            version_id=version_id,
            reference_page=reference_page,
            markups=markups,
            markup_types=markup_types,
        )

    async def delete_template_versions(self, document_type_id: str, version_ids: list[str]) -> ProxyResponse:
        return await self._template_proxy.delete_template_versions(
            document_type_id=document_type_id, version_ids=version_ids
        )

    async def save_extra_fields(self, document_type_id: str, name: str, order: int) -> ProxyResponse:
        return await self._enrichment_proxy.save_extra_fields(document_type_id=document_type_id, name=name, order=order)

    async def update_extra_fields(self, document_type_id: str, fields: list[ExtraFieldData]) -> ProxyResponse:
        return await self._enrichment_proxy.update_extra_fields(document_type_id=document_type_id, fields=fields)

    async def delete_extra_fields(self, document_type_id: str, extra_field_codes: list[str]) -> ProxyResponse:
        return await self._enrichment_proxy.delete_extra_fields(
            document_type_id=document_type_id,
            extra_field_codes=extra_field_codes,
        )

    async def save_profile(self, document_type_id: str, profile: ProfileData) -> ProxyResponse:
        return await self._output_exporting_proxy.save_profile(document_type_id=document_type_id, profile=profile)

    async def update_profile(self, document_type_id: str, profile_id: str, profile: ProfileData) -> ProxyResponse:
        return await self._output_exporting_proxy.update_profile(
            document_type_id=document_type_id,
            profile_id=profile_id,
            profile=profile,
        )

    async def delete_profile(self, document_type_id: str, profile_id: str) -> ProxyResponse:
        return await self._output_exporting_proxy.delete_profile(
            document_type_id=document_type_id,
            profile_id=profile_id,
        )

    async def create_azure_extractor(
        self,
        name: str,
        model_id: str,
        endpoint: str,
        api_key: str,
        language: Optional[str],
        description: Optional[str],
    ) -> ProxyResponse:
        return await self._cloud_native_extraction_proxy.create_azure_extractor(
            name=name,
            model_id=model_id,
            endpoint=endpoint,
            api_key=api_key,
            language=language,
            description=description,
        )

    async def get_azure_extractor_info(self, document_type_id: str) -> ProxyResponse:
        return await self._cloud_native_extraction_proxy.get_azure_extractor_info(document_type_id)

    async def validate_azure_credentials(self, endpoint: str, model_id: str, api_key: str) -> ProxyResponse:
        return await self._cloud_native_extraction_proxy.validate_credentials(
            endpoint=endpoint, model_id=model_id, api_key=api_key
        )

    async def update_azure_extractor(
        self,
        document_type_id: str,
        model_id: str,
        endpoint: str,
        api_key: str,
    ) -> ProxyResponse:
        return await self._cloud_native_extraction_proxy.update_azure_extractor(
            extractor_id=document_type_id,
            model_id=model_id,
            endpoint=endpoint,
            api_key=api_key,
        )

    async def azure_extractor_checkup(self, document_type_id: str) -> ProxyResponse:
        return await self._cloud_native_extraction_proxy.azure_extractor_checkup(document_type_id)

    async def synchronize_azure_extractor(self, document_type_id: str) -> ProxyResponse:
        return await self._cloud_native_extraction_proxy.synchronize_azure_extractor(document_type_id)

    async def get_all_validators(self, document_type_id: str) -> ProxyResponse:
        return await self._high_sparrow_proxy.get_all_validators(document_type_id)

    async def validate_field(
        self,
        document_type_id: str,
        validator_code: str,
        document_id: str,
    ) -> ProxyResponse:
        return await self._high_sparrow_proxy.validate_field(
            document_type_id=document_type_id,
            validator_code=validator_code,
            document_id=document_id,
        )

    async def add_extraction_query(
        self,
        extractor_id: str,
        document_type_id: str,
        code: str,
        shape: RawDataShape,
        workflow: RawLLMWorkflow,
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.add_extraction_query(
            extractor_id=extractor_id,
            document_type_id=document_type_id,
            code=code,
            shape=shape,
            workflow=workflow,
        )

    async def update_extraction_query(
        self,
        extractor_id: str,
        document_type_id: str,
        code: str,
        workflow: RawLLMWorkflow,
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.update_extraction_query(
            extractor_id=extractor_id,
            document_type_id=document_type_id,
            code=code,
            workflow=workflow,
        )

    async def create_llm_extractor(
        self,
        extractor_name: str,
        document_type_name: str,
        provider: str,
        model: str,
        extractor_id: Optional[str] = None,
        extraction_params: Optional[dict[str, Any]] = None,
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.create_llm_extractor(
            extractor_name=extractor_name,
            document_type_name=document_type_name,
            provider=provider,
            model=model,
            extraction_params=extraction_params,
            extractor_id=extractor_id,
        )

    async def update_llm_extractor(
        self,
        extractor_id: str,
        document_type_id: str,
        name: str,
        extraction_params: dict[str, Any],
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.update_llm_extractor(
            extractor_id=extractor_id,
            document_type_id=document_type_id,
            name=name,
            extraction_params=extraction_params,
        )

    async def assign_llm_to_llm_extractor(
        self,
        extractor_id: str,
        document_type_id: str,
        provider: str,
        model: str,
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.assign_llm_to_llm_extractor(
            extractor_id=extractor_id,
            document_type_id=document_type_id,
            provider=provider,
            model=model,
        )

    async def get_llm_extractors_for(self, document_type_id: str) -> ProxyResponse:
        return await self._ai_fusion_proxy.get_llm_extractors(document_type_id)

    async def detach_extractor(self, document_type_id: str, extractor_id: str) -> ProxyResponse:
        return await self._extraction_proxy.detach_extractor(
            document_type_id=document_type_id,
            extractor_id=extractor_id,
        )

    async def move_queries_between_extractors(
        self,
        source_extractor_id: str,
        target_extractor_id: str,
        document_type_id: str,
        fields_codes: list[str],
    ) -> ProxyResponse:
        return await self._ai_fusion_proxy.move_queries_between_extractors(
            source_extractor_id=source_extractor_id,
            target_extractor_id=target_extractor_id,
            document_type_id=document_type_id,
            fields_codes=fields_codes,
        )

    async def _gather_document_type_requests(
        self, document_type_id: str, extras: Optional[list[DocumentTypeExtras]]
    ) -> _DocumentTypeResponses:
        coroutines = {"document_type_response": self._document_type_proxy.get_document_type(document_type_id)}

        if extras is not None:
            if DocumentTypeExtras.EXTRACTION_FIELDS or DocumentTypeExtras.PROCESSING_PARAMS in extras:
                coroutines["extraction_response"] = self._extraction_proxy.get_document_type_v5(document_type_id)
            if DocumentTypeExtras.EXTRA_FIELDS in extras:
                coroutines["enrichment_response"] = self._enrichment_proxy.get_extra_fields(document_type_id)
            if DocumentTypeExtras.VALIDATORS in extras:
                coroutines["high_sparrow_response"] = self._high_sparrow_proxy.find_document_type(document_type_id)
            if DocumentTypeExtras.PROFILES in extras:
                coroutines["output_exporting_response"] = self._output_exporting_proxy.get_profiles(document_type_id)
            if DocumentTypeExtras.CLASSIFIERS in extras:
                coroutines[
                    "classification_response"
                ] = self._classification_proxy.get_gen_ai_classifiers_of_document_type(document_type_id)
            if DocumentTypeExtras.LLM_EXTRACTORS in extras:
                coroutines["ai_fusion_response"] = self._ai_fusion_proxy.get_llm_extractors(document_type_id)
            if DocumentTypeExtras.WORKFLOW_CONFIGURATIONS in extras:
                coroutines["workflow_manager_response"] = self._workflow_manager_proxy.get_workflow_configuration(
                    document_type_id
                )

        return _DocumentTypeResponses(
            zip(coroutines.keys(), await asyncio.gather(*coroutines.values()))  # type: ignore
        )

    async def _gather_get_prototype_requests(
        self,
        document_type_id: str,
        extras: Optional[list[GetPrototypeExtras]],
    ) -> _GetPrototypeResponses:
        coroutines = {
            "prototype_response": self._prototype_proxy.get_prototype(document_type_id),
            "extraction_response": self._extraction_proxy.get_extraction_document_type(document_type_id),
        }

        if extras is not None and GetPrototypeExtras.LAYOUTS in extras:
            coroutines["layouts_response"] = self._prototype_proxy.get_reference_layouts(document_type_id)

        return _GetPrototypeResponses(
            zip(coroutines.keys(), await asyncio.gather(*coroutines.values()))  # type: ignore
        )

    async def _gather_get_reference_layout_requests(
        self,
        document_type_id: str,
        layout_id: str,
    ) -> _GetReferenceLayoutResponses:
        coroutines = {
            "reference_layouts_response": self._prototype_proxy.get_reference_layout(
                document_type_id=document_type_id, layout_id=layout_id
            ),
            "unified_data_response": self._unifier_proxy.get_unified_data(document_id=layout_id),
            "document_layout_data_response": self._parsing_proxy.get_document_layout_info(layout_id=layout_id),
        }

        return _GetReferenceLayoutResponses(
            zip(coroutines.keys(), await asyncio.gather(*coroutines.values()))  # type: ignore
        )
