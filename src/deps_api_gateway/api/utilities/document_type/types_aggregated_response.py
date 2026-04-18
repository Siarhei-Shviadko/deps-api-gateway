import json
from functools import cached_property
from typing import Any, Union

from deps_api_gateway.domain.exceptions import DocumentTypeError

from .document_type_content import TypeContent

__all__ = ["TypesAggregatedResponse"]


class TypesAggregatedResponse:
    CORLEONE_INDEX: int = 0
    TYPE_INDEX: int = 1

    def __init__(self, finished_tasks: tuple[Union[Any, BaseException], Union[Any, BaseException]]):
        self._finished_tasks = finished_tasks
        self._validate()

    @cached_property
    def corleone(self) -> list[TypeContent]:
        return (
            []
            if self._is_invalid_content(self._finished_tasks[self.CORLEONE_INDEX])
            else [
                TypeContent.from_corleone_service(elem)
                for elem in self._finished_tasks[self.CORLEONE_INDEX]["result"]  # type: ignore
            ]
        )

    @cached_property
    def document_type(self) -> list[TypeContent]:
        return (
            []
            if self._is_invalid_content(self._finished_tasks[self.TYPE_INDEX])
            else [TypeContent.from_type_service(elem) for elem in self._finished_tasks[self.TYPE_INDEX]]  # type: ignore
        )

    @cached_property
    def types_length(self) -> int:
        return len(self.corleone) + len(self.document_type)

    @cached_property
    def all_types_json(self) -> str:
        return json.dumps(
            {
                "result": [type_content.to_dict() for type_content in self.corleone + self.document_type],
                "meta": {"total": self.types_length, "size": self.types_length},
            }
        )

    def _validate(self) -> None:
        if all(self._is_invalid_content(task) for task in self._finished_tasks):
            raise DocumentTypeError("Can't get document types")

    @staticmethod
    def _is_invalid_content(raw_content: Union[Any, Exception]) -> bool:
        return issubclass(type(raw_content), Exception)
