import json
from functools import cached_property
from typing import Any, Optional, Union

from deps_api_gateway.domain.exceptions import NotFoundError

from .document_type_content import TypeContent

TaskResult = Union[Any, BaseException]


__all__ = ["TypeRoutedResponse"]


class TypeRoutedResponse:
    def __init__(self, corleone_task_result: Optional[TaskResult], document_type_task_result: Optional[TaskResult]):
        self._corleone_task_result = corleone_task_result
        self._document_type_task_result = document_type_task_result
        self._validate()

    @cached_property
    def corleone(self) -> Optional[TypeContent]:
        return (
            None
            if self._corleone_task_failed()
            else TypeContent.from_corleone_service(self._corleone_task_result)  # type: ignore
        )

    @cached_property
    def document_type(self) -> Optional[TypeContent]:
        return (
            None
            if self._document_type_task_failed()
            else TypeContent.from_type_service(self._document_type_task_result)  # type: ignore
        )

    @cached_property
    def chosen_type_json(self) -> str:
        return json.dumps(self.document_type.to_dict() if self.document_type else self.corleone.to_dict())

    def _validate(self) -> None:
        if self._corleone_task_failed() and self._document_type_task_failed():
            raise NotFoundError("Document type was not found.")

    def _corleone_task_failed(self) -> bool:
        return not self._corleone_task_result or self._is_failed_task(self._corleone_task_result)

    def _document_type_task_failed(self) -> bool:
        return not self._document_type_task_result or self._is_failed_task(self._document_type_task_result)

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return issubclass(type(task_result), Exception)
