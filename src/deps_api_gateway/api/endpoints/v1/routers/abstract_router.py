import logging
import re
from abc import ABC
from typing import Any, Awaitable, Callable, Dict, Optional

from async_rest_client import Methods
from fastapi import Request, Response

from deps_api_gateway.api.utilities import ParsedRequest, ResponseBuilder
from deps_api_gateway.infrastructure import OldGenericRestClient

__all__ = ["AbstractRouter", "RequestMapper"]

RequestMapper = Dict[tuple[Methods, str], Callable[[Any], Awaitable[Any]]]  # noqa: WPS221


class AbstractRouter(ABC):
    def __init__(
        self,
        client: OldGenericRestClient,
    ) -> None:
        self._client = client
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def request_mapper(self) -> RequestMapper:
        return {}

    async def route(self, request: Request) -> Response:
        try:
            # Preload and cache the request body early.
            # Starlette streams the request body and allows it to be consumed only once.
            # If we don't preload here, later consumers (e.g., ParsedRequest,
            # request processors, or logging) may encounter race conditions or empty bodies.
            await request.body()

            parsed_request = ParsedRequest(request)
            request_processor = self.get_request_processor(parsed_request)

            if request_processor:
                return await request_processor(parsed_request)

            response = await self._client.request(**await parsed_request.to_dict())
            return (
                ResponseBuilder()
                .with_content(response["content"])
                .with_status(response["status_code"])
                .with_headers(response["headers"])
                .build()
            )
        except Exception:
            self._logger.debug("Request to the service failed.\n Failed request: %s.", request.__dict__)  # noqa: WPS609
            raise

    def get_request_processor(self, request: ParsedRequest) -> Optional[Callable]:
        for (method, url), processor in self.request_mapper.items():
            if request.method == method and re.match(url, request.url):
                return processor

        return None
