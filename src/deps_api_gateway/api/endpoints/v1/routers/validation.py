import logging
import re
from http import HTTPStatus

from async_rest_client import Methods
from fastapi.responses import Response

from deps_api_gateway.api.utilities import ParsedRequest, ResponseBuilder
from deps_api_gateway.application import IHighSparrowProxy
from deps_api_gateway.constants import V1_PREFIX, VALIDATION_BASE_PREFIX
from deps_api_gateway.domain.exceptions import ServiceUnavailableError
from deps_api_gateway.infrastructure.proxies import (
    HighSparrowServiceUnavailableError,
    OldGenericRestClient,
)

from .abstract_router import AbstractRouter, RequestMapper

__all__ = ["ValidationRouter"]


class ValidationRouter(AbstractRouter):
    def __init__(self, client: OldGenericRestClient, high_sparrow_proxy: IHighSparrowProxy):
        super().__init__(client)
        self._high_sparrow_proxy = high_sparrow_proxy

        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def request_mapper(self) -> RequestMapper:
        request_mapper: RequestMapper = {}
        request_mapper[
            (
                Methods.GET,
                rf"^{VALIDATION_BASE_PREFIX}{V1_PREFIX}/results/\w+$",
            )
        ] = self._validation_result
        return request_mapper

    async def _validation_result(self, request: ParsedRequest) -> Response:
        request_dict = await request.to_dict()

        match = re.match(rf"^{VALIDATION_BASE_PREFIX}{V1_PREFIX}/results/(?P<document_id>\w+)$", request_dict["url"])
        document_id = match.group("document_id")

        try:
            high_sparrow_response = await self._high_sparrow_proxy.get_validation_result(document_id)
        except HighSparrowServiceUnavailableError as high_sparrow_error:
            self._logger.exception(high_sparrow_error.code)
        else:
            if high_sparrow_response.status_code == HTTPStatus.OK:
                return (
                    ResponseBuilder()
                    .with_content(high_sparrow_response.content)
                    .with_status(high_sparrow_response.status_code)
                    .with_headers(high_sparrow_response.headers)
                    .build()
                )

        try:
            validation_response = await self._client.request(**request_dict)
        except Exception as validation_error:
            raise ServiceUnavailableError(validation_error)
        return (
            ResponseBuilder()
            .with_content(validation_response["content"])
            .with_status(validation_response["status_code"])
            .with_headers(validation_response["headers"])
            .build()
        )
