import json
from functools import cached_property
from typing import Any, Optional, Union

from fastapi import status

from deps_api_gateway.domain.exceptions import DocumentTypeError

__all__ = ["DocumentTypeResponse"]


TaskResult = Union[dict, BaseException]


class DocumentTypeResponse:
    def __init__(
        self,
        document_type_task_result: TaskResult,
        extraction_task_result: TaskResult,
    ) -> None:
        self._document_type_task_result = document_type_task_result
        self._extraction_task_result = extraction_task_result

        self._validate()

    @cached_property
    def document_type(self) -> Optional[dict]:
        return (
            None
            if self._document_type_task_result_failed()
            else json.loads(self._document_type_task_result["content"])  # type: ignore
        )

    @cached_property
    def extraction(self) -> Optional[dict]:
        return (
            None
            if self._extraction_task_failed()
            else json.loads(self._extraction_task_result["content"])  # type: ignore
        )

    def make_response(self) -> dict[str, Any]:
        self.document_type["fields"] = self.extraction["fields"]

        return self.document_type

    def _validate(self) -> None:
        if self._document_type_task_result_failed() or self._extraction_task_failed():
            raise DocumentTypeError("Can't get document type!")

    def _document_type_task_result_failed(self) -> bool:
        return self._is_failed_task(self._document_type_task_result)

    def _extraction_task_failed(self) -> bool:
        return self._is_failed_task(self._extraction_task_result)

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return isinstance(task_result, BaseException) or task_result.get("status_code") != status.HTTP_200_OK
