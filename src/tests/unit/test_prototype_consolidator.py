from deps_api_gateway.application.document_type import PrototypeConsolidator
from tests.data.extraction_json_data import *
from tests.data.prototype_json_data import *


def test_consolidation__field_with_mapping(ok_proxy_response__maker) -> None:
    raw_field_response = ok_proxy_response__maker(EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT)
    raw_mapping_response = ok_proxy_response__maker(PROTOTYPE_MAPPING_RESPONSE_DICT)

    consolidated_field = PrototypeConsolidator.consolidate_mapping_with_field(
        extraction_field_response=raw_field_response,
        prototype_mapping_response=raw_mapping_response,
    )

    assert consolidated_field.json() == EXPECTED_CONSOLIDATED__FIELD_WITH_MAPPING_DICT


def test_consolidation__both_not_ok__extraction_error_returned(not_ok_proxy_response__maker) -> None:
    raw_field_response = not_ok_proxy_response__maker(
        status_code=400,
        data=EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT,
    )
    raw_mapping_response = not_ok_proxy_response__maker(
        status_code=400,
        data=PROTOTYPE_MAPPING_RESPONSE_DICT,
    )

    consolidated_field = PrototypeConsolidator.consolidate_mapping_with_field(
        extraction_field_response=raw_field_response,
        prototype_mapping_response=raw_mapping_response,
    )

    assert consolidated_field == raw_field_response


def test_consolidation__extraction_ok__prototype_not_ok__prototype_error_returned(not_ok_proxy_response__maker) -> None:
    raw_field_response = not_ok_proxy_response__maker(
        status_code=200,
        data=EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT,
    )
    raw_mapping_response = not_ok_proxy_response__maker(
        status_code=400,
        data=PROTOTYPE_MAPPING_RESPONSE_DICT,
    )

    consolidated_field = PrototypeConsolidator.consolidate_mapping_with_field(
        extraction_field_response=raw_field_response,
        prototype_mapping_response=raw_mapping_response,
    )

    assert consolidated_field == raw_mapping_response


def test_consolidation__prototype_with_extraction_fields(ok_proxy_response__maker) -> None:
    raw_extraction_response = ok_proxy_response__maker(EXTRACTION_DOCUMENT_TYPE_RESPONSE_DICT)
    raw_prototype_response = ok_proxy_response__maker(PROTOTYPE_DOCUMENT_TYPE_RESPONSE__DICT)

    consolidated = PrototypeConsolidator.consolidate_prototype_with_extraction_fields(
        extraction_document_type_response=raw_extraction_response,
        prototype_response=raw_prototype_response,
    )

    assert consolidated.json() == EXPECTED_CONSOLIDATED__PROTOTYPE_WITH_EXTRACTION_RESPONSE_DICT
