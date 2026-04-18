from typing import Optional

from ..proxy_response import ProxyResponse
from .inclusion_params import DocumentTypeExtras


class DocumentTypeConsolidator:
    @classmethod
    def consolidate_document_types(
        cls, document_types_response: ProxyResponse, workflow_configurations_response: Optional[ProxyResponse]
    ) -> ProxyResponse:
        if not document_types_response.is_ok():
            return document_types_response

        workflow_configurations_dict: dict = {}
        if workflow_configurations_response is not None and workflow_configurations_response.is_ok():
            workflow_configurations_dict = workflow_configurations_response.json()  # type: ignore

        content: dict = document_types_response.json()  # type: ignore
        for document_type in content["result"]:
            del document_type["fields"]
            document_type["workflowConfiguration"] = workflow_configurations_dict.get(document_type["id"], None)

        return document_types_response.with_updated_content(
            status_code=document_types_response.status_code, content=content, headers=document_types_response.headers
        )

    @classmethod
    def consolidate_document_type(
        cls,
        document_type_response: ProxyResponse,
        extraction_response: Optional[ProxyResponse],
        enrichment_response: Optional[ProxyResponse],
        high_sparrow_response: Optional[ProxyResponse],
        output_exporting_response: Optional[ProxyResponse],
        classification_response: Optional[ProxyResponse],
        ai_fusion_response: Optional[ProxyResponse],
        workflow_manager_response: Optional[ProxyResponse],
        extras: Optional[list[DocumentTypeExtras]],
    ) -> ProxyResponse:
        failed_request = cls._validate_document_type_responses(
            document_type_response=document_type_response,
            extraction_response=extraction_response,
            enrichment_response=enrichment_response,
            high_sparrow_response=high_sparrow_response,
            output_exporting_response=output_exporting_response,
            classification_response=classification_response,
            ai_fusion_response=ai_fusion_response,
            workflow_manager_response=workflow_manager_response,
        )

        if failed_request is not None:
            return failed_request

        content = cls._enrich_document_type(
            document_type_response=document_type_response,
            extraction_response=extraction_response,
            enrichment_response=enrichment_response,
            high_sparrow_response=high_sparrow_response,
            output_exporting_response=output_exporting_response,
            classification_response=classification_response,
            ai_fusion_response=ai_fusion_response,
            workflow_manager_response=workflow_manager_response,
            extras=extras,
        )

        return document_type_response.with_updated_content(
            status_code=document_type_response.status_code, content=content, headers=document_type_response.headers
        )

    @classmethod
    def _enrich_document_type(
        cls,
        document_type_response: ProxyResponse,
        extraction_response: Optional[ProxyResponse],
        enrichment_response: Optional[ProxyResponse],
        high_sparrow_response: Optional[ProxyResponse],
        output_exporting_response: Optional[ProxyResponse],
        classification_response: Optional[ProxyResponse],
        ai_fusion_response: Optional[ProxyResponse],
        workflow_manager_response: Optional[ProxyResponse],
        extras: Optional[list[DocumentTypeExtras]],
    ) -> dict:
        document_type: dict = document_type_response.json()  # type: ignore
        extraction_fields = None

        del document_type["fields"]

        if extras:
            if DocumentTypeExtras.EXTRACTION_FIELDS in extras and extraction_response.is_ok():
                extraction_fields = extraction_response.json()["fields"]  # type: ignore

        if high_sparrow_response is None or high_sparrow_response.is_not_found():
            document_type["validators"] = None
            document_type["crossFieldValidators"] = None
        else:
            high_sparrow_response_dict = high_sparrow_response.json()
            document_type["validators"] = high_sparrow_response_dict["validators"]  # type: ignore
            document_type["crossFieldValidators"] = high_sparrow_response_dict["crossFieldValidators"]  # type: ignore

        document_type.update(
            {
                "extractionFields": extraction_fields,
                "extraFields": None
                if enrichment_response is None or enrichment_response.is_not_found()
                else enrichment_response.json()["fields"],  # type: ignore
                "profiles": None
                if output_exporting_response is None or output_exporting_response.is_not_found()
                else output_exporting_response.json()["profiles"],  # type: ignore
                "classifiers": None
                if classification_response is None or classification_response.is_not_found()
                else classification_response.json(),  # type: ignore
                "llmExtractors": None
                if ai_fusion_response is None or ai_fusion_response.is_not_found()
                else ai_fusion_response.json()["llmExtractors"],  # type: ignore
                "workflowConfiguration": None
                if workflow_manager_response is None or workflow_manager_response.is_not_found()
                else workflow_manager_response.json(),  # type: ignore
            },
        )

        return document_type

    @staticmethod
    def _validate_document_type_responses(
        document_type_response: ProxyResponse,
        extraction_response: Optional[ProxyResponse],
        enrichment_response: Optional[ProxyResponse],
        high_sparrow_response: Optional[ProxyResponse],
        output_exporting_response: Optional[ProxyResponse],
        classification_response: Optional[ProxyResponse],
        ai_fusion_response: Optional[ProxyResponse],
        workflow_manager_response: Optional[ProxyResponse],
    ) -> Optional[ProxyResponse]:
        if not document_type_response.is_ok():
            return document_type_response

        for response in (
            extraction_response,
            enrichment_response,
            high_sparrow_response,
            output_exporting_response,
            classification_response,
            ai_fusion_response,
            workflow_manager_response,
        ):
            if response is not None and DocumentTypeConsolidator._extra_response_invalid(response):
                return response

        return None

    @staticmethod
    def _extra_response_invalid(response: ProxyResponse) -> bool:
        return not (response.is_ok() or response.is_not_found())
