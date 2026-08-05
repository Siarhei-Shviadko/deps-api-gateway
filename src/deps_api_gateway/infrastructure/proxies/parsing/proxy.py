import json
from typing import Any, Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    IParsingProxy,
    PageBatch,
    ParsingFeature,
    ParsingType,
    ProxyResponse,
    ProxyResponseFactory,
    RawPoint,
)
from deps_api_gateway.constants import PARSING_BASE_API_PREFIX, V1_PREFIX, V2_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import ParsingProxyRequestError, ParsingServiceUnavailableError
from .get_page_batch_url_factory import GetPageBatchUrlFactory

__all__ = ["ParsingProxy"]


class ParsingProxy(GenericRestClient, IParsingProxy):
    v1_prefix = f"{PARSING_BASE_API_PREFIX}{V1_PREFIX}"
    v2_prefix = f"{PARSING_BASE_API_PREFIX}{V2_PREFIX}"
    exception = ParsingProxyRequestError

    async def find_document_layout(self, layout_id: str) -> dict[str, Any]:
        url = f"{self.v1_prefix}/document-layout/{layout_id}/info"
        return await self.request(method=Methods.GET, url=url)

    async def get_document_layout_info(self, layout_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-layout/{layout_id}/info"

        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def get_pages(
        self,
        document_layout_id: str,
        parsing_type: ParsingType,
        features: set[ParsingFeature],
        batch_index: int = PageBatch.index,
        batch_size: int = PageBatch.size,
    ) -> dict[str, Any]:
        url = f"{self.v1_prefix}/document-layout/{document_layout_id}/pages"
        url_factory = GetPageBatchUrlFactory(
            document_layout_id=document_layout_id,
            parsing_type=parsing_type,
            features=features,
            batch_index=batch_index,
            batch_size=batch_size,
        )

        response = await self.request(method=Methods.GET, url=url, params=url_factory.params())

        self._check_response(response=response, url=url)

        content = json.loads(response["content"])
        content["count"] = len(content["pages"])
        content["next"] = url_factory.next()
        content["previous"] = url_factory.previous()

        return content

    async def get_document_layout(
        self,
        document_layout_id: str,
        parsing_type: ParsingType,
        features: Optional[set[ParsingFeature]] = None,
        batch_index: Optional[int] = None,
        batch_size: Optional[int] = None,
    ) -> ProxyResponse:
        async with self._handling_exception(ParsingServiceUnavailableError):
            params: dict[str, Any] = {
                "parsingType": parsing_type.value,
            }
            if features is not None:
                params["features"] = [feature.value for feature in features]
            if batch_size is not None and batch_index is not None:
                params.update({"batchIndex": batch_index, "batchSize": batch_size})

            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.v2_prefix}/document-layout/{document_layout_id}",
                    params=params,
                ),
            )

    async def get_parsing_info(self, document_id: str) -> ProxyResponse:
        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.v2_prefix}/documents/{document_id}/parsing-info"),
            )

    async def get_engines(self, layout_type: str | None = None) -> ProxyResponse:
        async with self._handling_exception(ParsingServiceUnavailableError):
            params = {"layoutType": layout_type} if layout_type else {}
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.v2_prefix}/engines", params=params),
            )

    async def get_tabular_layout(
        self,
        tabular_layout_id: str,
        tables: Optional[list[str]],
        row_span: Optional[tuple[int, int]],
        col_span: Optional[tuple[int, int]],
    ) -> ProxyResponse:
        async with self._handling_exception(ParsingServiceUnavailableError):
            params_candidate = {"tables": tables, "rowSpan": row_span, "colSpan": col_span}
            params = {k: v for k, v in params_candidate.items() if v is not None}

            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.v2_prefix}/tabular-layout/{tabular_layout_id}",
                    params=params,
                )
            )

    async def clone_document_layout(self, document_id: str, parsing_type: str) -> ProxyResponse:
        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PUT,
                    url=f"{self.v2_prefix}/document-layout/{document_id}/user-parsing-type",
                    json={"parsingType": parsing_type},
                )
            )

    async def update_paragraph(
        self,
        document_layout_id: str,
        page_id: str,
        paragraph_id: str,
        update_paragraph_request: dict[str, Any],
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/document-layout/{document_layout_id}/pages/{page_id}/paragraphs/{paragraph_id}"
        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PATCH, url=url, json=update_paragraph_request)
            )

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
        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH,
                    url=f"{self.v2_prefix}/document-layout/{document_id}/pages/{page_id}/images/{image_id}",
                    json={
                        "title": title,
                        "description": description,
                        "filepath": filepath,
                        "polygon": polygon,
                    },
                )
            )

    async def update_table(
        self,
        document_layout_id: str,
        page_id: str,
        table_id: str,
        update_table_request: dict[str, Any],
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/document-layout/{document_layout_id}/pages/{page_id}/tables/{table_id}"
        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PATCH, url=url, json=update_table_request)
            )

    async def update_key_value_pair(
        self,
        document_layout_id: str,
        page_id: str,
        key_value_pair_id: str,
        update_key_value_pair_request: dict,
    ) -> ProxyResponse:
        url = (
            f"{self.v2_prefix}/document-layout/{document_layout_id}/pages/{page_id}/key-value-pairs/{key_value_pair_id}"
        )
        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PATCH, url=url, json=update_key_value_pair_request)
            )
