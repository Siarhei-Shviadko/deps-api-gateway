import json
from http import HTTPStatus

from async_rest_client import Methods
from fastapi.responses import Response

from deps_api_gateway.api.utilities import ParsedRequest, ResponseBuilder
from deps_api_gateway.application import ExtractorType
from deps_api_gateway.constants import (
    DOCUMENT_TYPE_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from deps_api_gateway.infrastructure import OldGenericRestClient
from deps_api_gateway.infrastructure.proxies import ExtractionProxy

from .abstract_router import AbstractRouter, RequestMapper

__all__ = ["DocumentTypeRouter"]


class DocumentTypeRouter(AbstractRouter):
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
            (Methods.POST, f"^{DOCUMENT_TYPE_BASE_API_PREFIX}{V2_PREFIX}/types"): self.attach_non_extractor,
            (
                Methods.POST,
                f"^{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/types/prototype",
            ): self.attach_prototype_extractor,
            (Methods.POST, f"^{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/types"): self.attach_template_extractor,
            (
                Methods.PUT,
                f"^{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/plugins/attach-extraction$",
            ): self.attach_plugin_extractor,
        }

    async def attach_non_extractor(self, request: ParsedRequest) -> Response:
        return await self._attach_extractor(request=request, extractor_type=ExtractorType.NON)

    async def attach_prototype_extractor(self, request: ParsedRequest) -> Response:
        return await self._attach_extractor(request=request, extractor_type=ExtractorType.PROTOTYPE)

    async def attach_template_extractor(self, request: ParsedRequest) -> Response:
        return await self._attach_extractor(request=request, extractor_type=ExtractorType.TEMPLATE)

    async def attach_plugin_extractor(self, request: ParsedRequest) -> Response:
        request_dict = await request.to_dict()
        extractor_data = json.loads(request_dict["data"].decode("utf-8"))
        extractor_plugin = extractor_data["plugin"]

        proxy_response = await self._extraction_proxy.attach_extractor(
            name=extractor_data["documentType"],
            extractor_type=ExtractorType.PLUGIN,
            fields=extractor_plugin.get("fields"),
            description=extractor_plugin.get("description"),
            engine=extractor_plugin.get("engine"),
            language=extractor_plugin.get("language"),
            image_transformations=extractor_plugin.get("imageTransformations"),
        )

        response_builder = ResponseBuilder().with_headers(proxy_response.headers).with_content(proxy_response.content)
        if proxy_response.status_code == HTTPStatus.CREATED:
            response_builder.with_status(HTTPStatus.OK)
        else:
            response_builder.with_status(proxy_response.status_code)

        return response_builder.build()

    async def _attach_extractor(self, request: ParsedRequest, extractor_type: ExtractorType) -> Response:
        request_dict = await request.to_dict()
        extractor_data = json.loads(request_dict["data"].decode("utf-8"))

        proxy_response = await self._extraction_proxy.attach_extractor(
            name=extractor_data["name"],
            extractor_type=extractor_type,
            language=extractor_data.get("language"),
            engine=extractor_data.get("engine"),
            description=extractor_data.get("description"),
        )
        return (
            ResponseBuilder()
            .with_status(proxy_response.status_code)
            .with_headers(proxy_response.headers)
            .with_content(proxy_response.content)
            .build()
        )
