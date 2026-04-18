import json
import re
from typing import Any

from async_rest_client import Methods
from fastapi.responses import Response

from deps_api_gateway.api.utilities import ParsedRequest, ResponseBuilder
from deps_api_gateway.application import FieldType
from deps_api_gateway.constants import TEMPLATE_BASE_API_PREFIX, V1_PREFIX
from deps_api_gateway.infrastructure import OldGenericRestClient
from deps_api_gateway.infrastructure.proxies import ExtractionProxy

from .abstract_router import AbstractRouter, RequestMapper

__all__ = ["TemplateRouter"]


class TemplateRouter(AbstractRouter):
    def __init__(
        self,
        client: OldGenericRestClient,
        extraction_proxy: ExtractionProxy,
    ) -> None:
        super().__init__(client)
        self._extraction_proxy = extraction_proxy

    @property
    def request_mapper(self) -> RequestMapper:
        return {
            (Methods.GET, rf"^{TEMPLATE_BASE_API_PREFIX}{V1_PREFIX}/templates/\w+/fields$"): self._get_template_fields,
            (
                Methods.POST,
                rf"^{TEMPLATE_BASE_API_PREFIX}{V1_PREFIX}/templates/\w+/fields$",
            ): self._create_template_field,
            (
                Methods.PATCH,
                rf"^{TEMPLATE_BASE_API_PREFIX}{V1_PREFIX}/templates/\w+/fields/\w+$",
            ): self._update_template_field,
            (
                Methods.DELETE,
                rf"^{TEMPLATE_BASE_API_PREFIX}{V1_PREFIX}/templates/\w+/fields/\w+$",
            ): self._delete_template_field,
        }

    async def _get_template_fields(self, request: ParsedRequest) -> Response:
        template_id = self._get_template_id_from_url(request.url)

        proxy_response = await self._extraction_proxy.get_document_type(document_type_id=template_id)

        data: dict[str, Any] = json.loads(proxy_response["content"].decode("utf-8"))
        fields: list[dict[str, Any]] = data["fields"]

        for field in fields:
            if field["promptValue"] is not None:
                fields.remove(field)

            field["id"] = field.pop("pk")
            field["type"] = field.pop("fieldType")
            field["description"] = field.pop("fieldMeta")
            field["templateId"] = template_id

        return ResponseBuilder().with_content(fields).with_status(proxy_response["status_code"]).build()

    async def _create_template_field(self, request: ParsedRequest) -> Response:
        template_id = self._get_template_id_from_url(request.url)
        request_dict = await request.to_dict()
        field_data = json.loads(request_dict["data"].decode("utf-8"))

        proxy_response = await self._extraction_proxy.create_field(
            document_type_id=template_id,
            name=field_data["name"],
            field_type=FieldType(field_data["type"]),
            description=field_data.get("description"),
            required=field_data["required"],
            confidential=field_data["confidential"],
            read_only=field_data["readOnly"],
            order=field_data.get("order", 0),
            extractor_id=field_data.get("extractorId"),
            field_code=field_data.get("code"),
        )
        return (
            ResponseBuilder()
            .with_status(proxy_response.status_code)
            .with_headers(proxy_response.headers)
            .with_content(proxy_response.content)
            .build()
        )

    async def _update_template_field(self, request: ParsedRequest) -> Response:
        template_id = self._get_template_id_from_url(request.url)
        field_code = self._get_field_code_from_url(request.url)
        request_dict = await request.to_dict()
        field_data = json.loads(request_dict["data"].decode("utf-8"))

        proxy_response = await self._extraction_proxy.update_field(
            document_type_id=template_id,
            field_code=field_code,
            name=field_data.get("name"),
            description=field_data.get("description"),
            required=field_data.get("required"),
            confidential=field_data.get("confidential"),
            read_only=field_data.get("readOnly"),
            order=field_data.get("order"),
            extractor_id=field_data.get("extractorId"),
        )
        return (
            ResponseBuilder()
            .with_status(proxy_response.status_code)
            .with_headers(proxy_response.headers)
            .with_content(proxy_response.content)
            .build()
        )

    async def _delete_template_field(self, request: ParsedRequest) -> Response:
        template_id = self._get_template_id_from_url(request.url)
        field_code = self._get_field_code_from_url(request.url)

        proxy_response = await self._extraction_proxy.delete_fields(
            document_type_id=template_id,
            field_codes=[field_code],
        )
        return (
            ResponseBuilder()
            .with_status(proxy_response.status_code)
            .with_headers(proxy_response.headers)
            .with_content(proxy_response.content)
            .build()
        )

    def _get_template_id_from_url(self, url: str) -> str:
        return re.search(r"(?<=templates\/).*(?=\/fields)", url)[0]

    def _get_field_code_from_url(self, url: str) -> str:
        return re.search(r"(?<=fields\/).*(?=)", url)[0]
