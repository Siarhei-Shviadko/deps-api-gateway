import re
from typing import Any

from deps_api_gateway.application import FieldType, ProxyResponse

from .....utilities.parsed_request import ParsedRequest

__all__ = ["PrototypeRouterHelper"]


class PrototypeRouterHelper:
    @staticmethod
    def extract_prototype_id_from_url(url: str) -> str:
        return re.search(r"prototypes/(\w+)", url).group(1)

    @staticmethod
    def extract_field_code_from_url(url: str) -> str:
        return re.search(r"fields/(\w+)", url).group(1)

    @staticmethod
    def extract_field_codes_from_request(request: ParsedRequest) -> list[str]:
        return request._request.query_params.get("fieldIds", [])

    @staticmethod
    def update_field_data_according_for_one2many_mapping(data: dict[str, Any]) -> dict[str, Any]:
        data["description"] = {
            "baseType": data["typeCode"],
            "baseTypeMeta": data["description"],
        }
        data["typeCode"] = FieldType.LIST.value

        return data

    @staticmethod
    def replace_lists_with_mapping_data_types(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        raw_response: dict = response.json()  # type: ignore
        for raw_field in raw_response["fields"]:
            if raw_field["fieldType"]["typeCode"] == FieldType.LIST.value:
                raw_field["fieldType"]["typeCode"] = raw_field["mapping"]["mappingDataType"]

        return ProxyResponse.with_updated_content(
            status_code=response.status_code,
            content=raw_response,
            headers=response.headers,
        )
