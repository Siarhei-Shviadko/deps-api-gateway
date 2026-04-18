import logging

from async_rest_client import Methods
from fastapi.responses import Response

from deps_api_gateway.api.endpoints.v1.routers.abstract_router import (
    AbstractRouter,
    RequestMapper,
)
from deps_api_gateway.api.utilities import ParsedRequest, ResponseBuilder
from deps_api_gateway.application import (
    FieldType,
    IExtraction,
    IPrototypeProxy,
    MappingType,
    PrototypeConsolidator,
    PrototypeDataTypeCode,
    ProxyResponse,
)
from deps_api_gateway.constants import PROTOTYPE_BASE_API_PREFIX, V1_PREFIX
from deps_api_gateway.infrastructure import OldGenericRestClient

from .helper import PrototypeRouterHelper

__all__ = ["PrototypeRouter"]


class PrototypeRouter(AbstractRouter):
    def __init__(
        self,
        client: OldGenericRestClient,
        extraction_proxy: IExtraction,
        prototype_proxy: IPrototypeProxy,
    ) -> None:
        super().__init__(client)
        self._prototype_proxy = prototype_proxy
        self._extraction_proxy = extraction_proxy

        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def request_mapper(self) -> RequestMapper:
        return {
            (Methods.GET, rf"^{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes/\w+$"): self._get_prototype,
            (Methods.POST, rf"^{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes/\w+/fields$"): self._create_field,
            (Methods.PATCH, rf"^{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes/\w+/fields/\w+$"): self._update_field,
            (
                Methods.DELETE,
                rf"^{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes/\w+/fields/\w+$",
            ): self._delete_field,
            (Methods.DELETE, rf"^{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes/\w+/fields$"): self._delete_fields,
            (
                Methods.PUT,
                rf"^{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes/\w+/fields/\w+/mapping$",
            ): self._update_mapping,
        }

    async def _create_field(self, request: ParsedRequest) -> Response:
        data = await request.json_data

        document_type_id = PrototypeRouterHelper.extract_prototype_id_from_url(request.url)

        # This freaking logic is a legacy piece of sh*t and will be performed on frontend when switch to v5 endpoints;
        # For now, for backward compatibility, we need to change Field Type to list if it's OneToMany
        mapping_data_type: str = data["typeCode"]
        if data.get("mappingType") == MappingType.ONE_TO_MANY:
            data = PrototypeRouterHelper.update_field_data_according_for_one2many_mapping(data)

        create_ef_response = await self._extraction_proxy.create_field(
            document_type_id=document_type_id,
            name=data["name"],
            field_type=FieldType(data["typeCode"]),
            description=data.get("description"),
            required=data["required"],
            confidential=data["confidential"],
            read_only=data["readOnly"],
            order=data.get("order", 0),
            extractor_id=data.get("extractorId"),
            field_code=data.get("code"),
        )

        created_field_code: str = create_ef_response.json()["code"]  # type: ignore

        create_mapping_response = None
        if create_ef_response.is_ok():
            create_mapping_response = await self._prototype_proxy.create_mapping(
                document_type_id=document_type_id,
                code=created_field_code,
                data_type=PrototypeDataTypeCode(mapping_data_type),
                keys=data["keys"],
                mapping_type=MappingType(data["mappingType"]),
            )

            if not create_mapping_response.is_ok():
                await self._extraction_proxy.delete_fields(
                    document_type_id=document_type_id,
                    field_codes=[created_field_code],
                )

        response: ProxyResponse = PrototypeConsolidator.consolidate_mapping_with_field(
            extraction_field_response=create_ef_response,
            prototype_mapping_response=create_mapping_response,
        )

        return (
            ResponseBuilder()
            .with_content(response.content)
            .with_status(response.status_code)
            .with_headers(response.headers)
            .build()
        )

    async def _update_field(self, request: ParsedRequest) -> Response:
        data = await request.json_data

        document_type_id = PrototypeRouterHelper.extract_prototype_id_from_url(request.url)
        field_code = PrototypeRouterHelper.extract_field_code_from_url(request.url)

        update_ef_response = await self._extraction_proxy.update_field(
            document_type_id=document_type_id,
            field_code=field_code,
            name=data.get("name"),
            description=data.get("description"),
            required=data.get("required"),
            confidential=data.get("confidential"),
            read_only=data.get("readOnly"),
            order=data.get("order"),
            extractor_id=data.get("extractorId"),
        )

        return (
            ResponseBuilder()
            .with_content(update_ef_response.content)
            .with_status(update_ef_response.status_code)
            .with_headers(update_ef_response.headers)
            .build()
        )

    async def _update_mapping(self, request: ParsedRequest) -> Response:
        data = await request.json_data

        document_type_id = PrototypeRouterHelper.extract_prototype_id_from_url(request.url)
        field_code = PrototypeRouterHelper.extract_field_code_from_url(request.url)

        update_mapping_response = await self._prototype_proxy.update_mapping(
            document_type_id=document_type_id,
            code=field_code,
            keys=data["keys"],
        )

        return (
            ResponseBuilder()
            .with_content(update_mapping_response.content)
            .with_status(update_mapping_response.status_code)
            .with_headers(update_mapping_response.headers)
            .build()
        )

    async def _delete_field(self, request: ParsedRequest) -> Response:
        document_type_id = PrototypeRouterHelper.extract_prototype_id_from_url(request.url)
        field_code = PrototypeRouterHelper.extract_field_code_from_url(request.url)

        delete_field_response = await self._extraction_proxy.delete_fields(
            document_type_id=document_type_id,
            field_codes=[field_code],
        )

        return (
            ResponseBuilder()
            .with_content(delete_field_response.content)
            .with_status(delete_field_response.status_code)
            .with_headers(delete_field_response.headers)
            .build()
        )

    async def _delete_fields(self, request: ParsedRequest) -> Response:
        document_type_id = PrototypeRouterHelper.extract_prototype_id_from_url(request.url)
        fields_from_query = PrototypeRouterHelper.extract_field_codes_from_request(request)

        delete_field_response = await self._extraction_proxy.delete_fields(
            document_type_id=document_type_id,
            field_codes=fields_from_query,
        )

        return (
            ResponseBuilder()
            .with_content(delete_field_response.content)
            .with_status(delete_field_response.status_code)
            .with_headers(delete_field_response.headers)
            .build()
        )

    async def _get_prototype(self, request: ParsedRequest) -> Response:
        document_type_id = PrototypeRouterHelper.extract_prototype_id_from_url(request.url)

        prototype_response = await self._prototype_proxy.get_prototype(
            document_type_id=document_type_id,
        )
        document_type_response = await self._extraction_proxy.get_extraction_document_type(
            document_type_id=document_type_id,
        )

        response = PrototypeConsolidator.consolidate_prototype_with_extraction_fields(
            extraction_document_type_response=document_type_response,
            prototype_response=prototype_response,
        )

        # Temporary logic to handle One2Many fields - Frontend expects FieldType NOT to be List, but baseType;
        # This will be removed in new v5 contract;
        response = PrototypeRouterHelper.replace_lists_with_mapping_data_types(response)

        return (
            ResponseBuilder()
            .with_content(response.content)
            .with_status(response.status_code)
            .with_headers(response.headers)
            .build()
        )
