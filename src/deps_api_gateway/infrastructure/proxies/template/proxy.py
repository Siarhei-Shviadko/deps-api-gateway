from async_rest_client import Methods

from deps_api_gateway.application import (
    ITemplateProxy,
    ProxyResponse,
    ProxyResponseFactory,
    TemplateDataTypeCode,
)
from deps_api_gateway.constants import TEMPLATE_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import TemplateServiceUnavailableError

__all__ = ["TemplateProxy"]


class TemplateProxy(GenericRestClient, ITemplateProxy):
    exception = TemplateServiceUnavailableError
    v1_prefix = f"{TEMPLATE_BASE_API_PREFIX}{V1_PREFIX}"

    async def get_template_versions(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/templates/{document_type_id}/versions"

        try:
            response = await self.request(method=Methods.GET, url=url)
        except Exception as error:
            raise TemplateServiceUnavailableError(error)

        return ProxyResponse(
            status_code=response["status_code"],
            content=response["content"],
            headers=response["headers"],
        )

    async def get_template_version(self, document_type_id: str, version_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/templates/{document_type_id}/versions/{version_id}"

        try:
            response = await self.request(method=Methods.GET, url=url)
        except Exception as error:
            raise TemplateServiceUnavailableError(error)

        return ProxyResponse(
            status_code=response["status_code"],
            content=response["content"],
            headers=response["headers"],
        )

    async def update_template_version(self, document_type_id: str, version_id: str, name: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/templates/{document_type_id}/versions/{version_id}/name"

        data = {"name": name}

        try:
            response = await self.request(method=Methods.PATCH, url=url, json=data)
        except Exception as error:
            raise TemplateServiceUnavailableError(error)

        return ProxyResponse(
            status_code=response["status_code"],
            content=response["content"],
            headers=response["headers"],
        )

    async def delete_template_versions(self, document_type_id: str, version_ids: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/templates/{document_type_id}/versions"

        try:
            response = await self.request(method=Methods.DELETE, url=url, json=version_ids)
        except Exception as error:
            raise TemplateServiceUnavailableError(error)

        return ProxyResponse(
            status_code=response["status_code"],
            content=response["content"],
            headers=response["headers"],
        )

    async def add_markup(
        self,
        document_type_id: str,
        version_id: str,
        reference_page: str,
        markups: dict[str, list[list[float]]],
        markup_types: dict[str, TemplateDataTypeCode],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/templates/{document_type_id}/versions/{version_id}/markups"

        data = {
            "referencePage": reference_page,
            "markups": markups,
            "markupTypes": markup_types,
        }

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))
