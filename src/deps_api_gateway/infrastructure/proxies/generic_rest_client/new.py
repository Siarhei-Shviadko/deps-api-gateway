from http import HTTPStatus
from types import TracebackType
from typing import Any, Optional

from async_rest_client import (
    AbstractRestClient,
    AsyncRestClientError,
    DEPSTokenAuthProvider,
)

from ...access_management import user

__all__ = ["GenericRestClient"]


class GenericRestClient(AbstractRestClient):
    exception: type[AsyncRestClientError]

    def _set_authentication(self) -> None:
        self._auth_provider = DEPSTokenAuthProvider(user)

    def _check_response(self, response: dict[str, Any], url: str) -> None:
        response_status_code = response["status_code"]
        response_content = response["content"]
        if response_status_code >= HTTPStatus.BAD_REQUEST:
            self._logger.error(
                "Response for url `%s` with status code `%s` failed with error %s",
                url,
                response_status_code,
                response_content,
            )

            raise self.exception(response_content)

    def _handling_exception(self, exception: Optional[type[BaseException]] = None):
        return self._ExceptionHandler(exception or self.exception)

    class _ExceptionHandler:
        def __init__(self, exception: type[BaseException]) -> None:
            self._exception = exception

        async def __aenter__(self):
            return self

        async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
        ):
            if exc_val:
                raise self._exception(exc_val)
