import json
from functools import cached_property
from typing import Any, Optional, Union

from fastapi import status
from pydantic import BaseModel, ConfigDict

from deps_api_gateway.domain.exceptions import DocumentTypeError

__all__ = ["DocumentTypesResponse"]


TaskResult = Union[dict, BaseException]


class DocumentTypesResponseData(BaseModel):
    result: list[dict[str, Any]]  # noqa: WPS110

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class DocumentTypesResponse:
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
            else json.loads(self._document_type_task_result["content"])["result"]  # type: ignore
        )

    @cached_property
    def extraction(self) -> Optional[dict]:
        return (
            None
            if self._extraction_task_failed()
            else json.loads(self._extraction_task_result["content"])["result"]  # type: ignore
        )

    def extraction_fields_by_id(self, id_: str) -> list[dict[str, Any]]:
        return next(
            (
                extraction_doc_type["fields"]
                for extraction_doc_type in self.extraction
                if extraction_doc_type["id"] == id_
            ),
            None,
        )

    def make_response(self) -> list[dict[str, Any]]:
        return self._combine_results()

    def _validate(self) -> None:
        if self._document_type_task_result_failed() or self._extraction_task_failed():
            raise DocumentTypeError("Can't get document types!")

    def _document_type_task_result_failed(self) -> bool:
        return self._is_failed_task(self._document_type_task_result)

    def _extraction_task_failed(self) -> bool:
        return self._is_failed_task(self._extraction_task_result)

    def _combine_results(self) -> list[dict[str, Any]]:
        combined_results = []

        for document_type in self.document_type:
            extraction_fields = self.extraction_fields_by_id(document_type["id"])

            document_type["fields"] = extraction_fields

            combined_results.append(document_type)

        return combined_results

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return isinstance(task_result, BaseException) or task_result.get("status_code") != status.HTTP_200_OK
