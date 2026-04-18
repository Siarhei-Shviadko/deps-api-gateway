from typing import Any, Optional

from ...proxy_response import ProxyResponse

__all__ = ["PrototypeConsolidator"]


class PrototypeConsolidator:
    @staticmethod
    def consolidate_mapping_with_field(
        extraction_field_response: ProxyResponse,
        prototype_mapping_response: ProxyResponse,
    ) -> ProxyResponse:
        if not extraction_field_response.is_ok():
            return extraction_field_response
        if not prototype_mapping_response.is_ok():
            return prototype_mapping_response

        consolidated_field = PrototypeConsolidator.consolidate_ef_with_mapping(
            raw_extraction_field=extraction_field_response.json(),  # type: ignore
            raw_mapping=prototype_mapping_response.json(),  # type: ignore
        )

        return ProxyResponse.with_updated_content(
            status_code=extraction_field_response.status_code,
            content=consolidated_field,
            headers=extraction_field_response.headers,
        )

    @staticmethod
    def consolidate_prototype_with_extraction_fields(
        extraction_document_type_response: ProxyResponse,
        prototype_response: ProxyResponse,
    ) -> ProxyResponse:
        if not extraction_document_type_response.is_ok():
            return extraction_document_type_response
        if not prototype_response.is_ok():
            return prototype_response

        raw_prototype: dict = prototype_response.json()  # type: ignore
        raw_document_type: dict = extraction_document_type_response.json()  # type: ignore

        consolidated_extraction_fields: list[dict[str, Any]] = []
        consolidated_table_fields: list[dict[str, Any]] = []

        mappings = raw_prototype.pop("mappings", [])
        tabular_mappings = raw_prototype.pop("tabularMappings", [])
        extraction_fields = raw_document_type.get("fields", [])

        for field in extraction_fields:
            field_code = field["code"]
            mapping = next((mapping for mapping in mappings if mapping["code"] == field_code), None)

            if mapping is not None:
                consolidated_extraction_fields.append(
                    PrototypeConsolidator.consolidate_ef_with_mapping(raw_extraction_field=field, raw_mapping=mapping),
                )
                continue

            tabular_mapping = next(
                (tabular_mapping for tabular_mapping in tabular_mappings if tabular_mapping["code"] == field_code),
                None,
            )

            if tabular_mapping is not None:
                consolidated_table_fields.append(
                    PrototypeConsolidator.consolidate_ef_with_tabular_mapping(
                        raw_extraction_field=field,
                        raw_tabular_mapping=tabular_mapping,
                    ),
                )

            # Fields without mappings can exist (prompted-fields for instance);
            # But those fields ain't part of Document-Type Prototype therefore we skip them here;

        consolidated_prototype = {
            **raw_prototype,
            "fields": consolidated_extraction_fields,
            "tableFields": consolidated_table_fields,
        }

        return ProxyResponse.with_updated_content(
            status_code=extraction_document_type_response.status_code,
            content=consolidated_prototype,
            headers=extraction_document_type_response.headers,
        )

    @staticmethod
    def consolidate_prototype(
        extraction_response: ProxyResponse,
        prototype_response: ProxyResponse,
        layouts_response: Optional[ProxyResponse],
    ) -> ProxyResponse:
        if layouts_response is not None and PrototypeConsolidator._extra_response_invalid(layouts_response):
            return layouts_response

        consolidated_prototype = PrototypeConsolidator.consolidate_prototype_with_extraction_fields(
            extraction_document_type_response=extraction_response,
            prototype_response=prototype_response,
        )
        consolidated_prototype_content = {
            **consolidated_prototype.json(),  # type: ignore
            "referenceLayouts": (
                layouts_response.json()["reference_layouts"]  # type: ignore
                if layouts_response is not None and layouts_response.is_ok()
                else None
            ),
        }

        return ProxyResponse.with_updated_content(
            status_code=consolidated_prototype.status_code,
            content=consolidated_prototype_content,
            headers=consolidated_prototype.headers,
        )

    @staticmethod
    def consolidate_ef_with_mapping(
        raw_extraction_field: dict[str, Any],
        raw_mapping: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "id": raw_extraction_field["code"],
            "prototypeId": raw_mapping["prototypeId"],
            "name": raw_extraction_field["name"],
            "fieldType": {
                "typeCode": raw_extraction_field["fieldType"],
                "description": raw_extraction_field["fieldMeta"],
            },
            "mapping": {
                "keys": raw_mapping["keys"],
                "mappingDataType": raw_mapping["dataType"],
                "mappingType": raw_mapping["mappingType"],
            },
            "required": raw_extraction_field["required"],
            "confidential": raw_extraction_field["confidential"],
            "readOnly": raw_extraction_field["readOnly"],
            "order": raw_extraction_field["order"],
        }

    @staticmethod
    def consolidate_ef_with_tabular_mapping(
        raw_extraction_field: dict[str, Any],
        raw_tabular_mapping: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "id": raw_extraction_field["code"],
            "prototypeId": raw_tabular_mapping["prototypeId"],
            "name": raw_extraction_field["name"],
            "fieldType": {
                "typeCode": raw_extraction_field["fieldType"],
                "description": raw_extraction_field["fieldMeta"],
            },
            "tabularMapping": {
                "headers": raw_tabular_mapping["headers"],
                "headerType": raw_tabular_mapping["headerType"],
                "occurrenceIndex": raw_tabular_mapping["occurrenceIndex"],
            },
            "required": raw_extraction_field["required"],
            "confidential": raw_extraction_field["confidential"],
            "readOnly": raw_extraction_field["readOnly"],
            "order": raw_extraction_field["order"],
        }

    @staticmethod
    def consolidate_reference_layout(
        reference_layout_response: ProxyResponse,
        unified_data_response: ProxyResponse | None,
        document_layout_data_response: ProxyResponse | None,
    ) -> ProxyResponse:
        content = {
            **reference_layout_response.json(),  # type: ignore
            "unifiedData": unified_data_response.json() if unified_data_response is not None else None,
            "documentLayoutData": document_layout_data_response.json()
            if document_layout_data_response is not None
            else None,
        }
        return reference_layout_response.with_updated_content(
            status_code=reference_layout_response.status_code,
            content=content,
            headers=reference_layout_response.headers,
        )

    @staticmethod
    def _extra_response_invalid(response: ProxyResponse) -> bool:
        return not (response.is_ok() or response.is_not_found())
