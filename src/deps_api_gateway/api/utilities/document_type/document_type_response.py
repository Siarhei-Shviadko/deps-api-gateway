# type: ignore
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Optional, Union

from deps_api_gateway.domain.exceptions import DocumentTypeError, NotFoundError

__all__ = ["DocumentType", "DocumentTypeRoutedResponse", "DocumentTypeAggregatedResponse"]


TaskResult = Union[Any, BaseException]


@dataclass
class DocumentType:
    id: str
    code: str
    name: str
    engine: str
    language: str
    fields: list[dict[str, Any]]
    description: Optional[str]
    created_at: Optional[str]

    @classmethod
    def from_corleone(cls, raw_response: dict[str, Any]) -> "DocumentType":
        return cls(
            id=raw_response["pk"],
            code=raw_response["code"],
            name=raw_response["name"],
            engine=raw_response["engine"],
            language=raw_response["language"],
            fields=raw_response.get("fields", []),
            description=raw_response.get("description"),
            created_at=raw_response.get("createdAt"),
        )

    @classmethod
    def from_document_type(cls, raw_response: dict[str, Any]) -> "DocumentType":
        return cls(
            id=raw_response["id"],
            code=raw_response["id"],
            name=raw_response["documentType"],
            engine=raw_response.get("engine"),
            language=raw_response.get("language"),
            fields=raw_response.get("fields", []),
            description=raw_response.get("description"),
            created_at=raw_response.get("created_at"),
        )

    def to_short_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "engine": self.engine,
            "language": self.language,
            "description": self.description,
            "createdAt": self.created_at,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "engine": self.engine,
            "language": self.language,
            "fields": self.fields,
            "description": self.description,
            "createdAt": self.created_at,
        }


class DocumentTypeRoutedResponse:
    def __init__(
        self,
        corleone_task_result: Optional[TaskResult] = None,
        document_type_task_result: Optional[TaskResult] = None,
    ) -> None:
        self._corleone_task_result = corleone_task_result
        self._document_type_task_result = document_type_task_result

        self._validate()

    @cached_property
    def chosen_plugin(self) -> dict[str, Any]:
        return (self.document_type or self.corleone).to_dict()

    @cached_property
    def corleone(self) -> Optional[DocumentType]:
        return None if self._corleone_task_failed() else DocumentType.from_corleone(self._corleone_task_result)

    @cached_property
    def document_type(self) -> Optional[DocumentType]:
        return (
            None
            if self._document_type_task_failed()
            else DocumentType.from_document_type(self._document_type_task_result)
        )

    def _validate(self) -> None:
        if self._corleone_task_failed() and self._document_type_task_failed():
            raise NotFoundError("Document type was not found.")

    def _corleone_task_failed(self) -> bool:
        return not self._corleone_task_result or self._is_failed_task(self._corleone_task_result)

    def _document_type_task_failed(self) -> bool:
        return not self._document_type_task_result or self._is_failed_task(self._document_type_task_result)

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return isinstance(task_result, Exception)


class DocumentTypeAggregatedResponse:
    def __init__(
        self,
        corleone_task_result: TaskResult,
        document_type_task_result: TaskResult,
    ) -> None:
        self._corleone_task_result = corleone_task_result
        self._document_type_task_result = document_type_task_result

        self._validate()

    @cached_property
    def corleone(self) -> list[DocumentType]:
        if self._corleone_task_failed():
            return []
        return [DocumentType.from_corleone(elem) for elem in self._corleone_task_result["result"]]

    @cached_property
    def document_type(self) -> list[DocumentType]:
        if self._document_type_task_failed():
            return []
        return [DocumentType.from_document_type(elem) for elem in self._document_type_task_result]

    @cached_property
    def all_plugins(self) -> list[dict[str, Any]]:
        return [plugin.to_short_dict() for plugin in self.corleone + self.document_type]

    def _validate(self) -> None:
        if self._corleone_task_failed() and self._document_type_task_failed():
            raise DocumentTypeError("Can't get document types!")

    def _corleone_task_failed(self) -> bool:
        return self._is_failed_task(self._corleone_task_result)

    def _document_type_task_failed(self) -> bool:
        return self._is_failed_task(self._document_type_task_result)

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return isinstance(task_result, Exception)
