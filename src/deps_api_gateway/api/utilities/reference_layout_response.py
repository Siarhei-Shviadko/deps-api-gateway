import json
from functools import cached_property
from http import HTTPStatus
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from deps_api_gateway.domain.exceptions import NotFoundError

TaskResult = Union[dict, BaseException]


__all__ = ["ReferenceLayoutResponse"]


class ReferenceLayoutResponseData(BaseModel):
    id: str
    prototype_id: str = Field(..., alias="prototypeId")
    title: Optional[str] = None
    state: str
    blob_name: str = Field(..., alias="blobName")
    unified_data: Optional[dict[str, Any]] = Field(..., alias="unifiedData")
    document_layout_data: Optional[dict[str, Any]] = Field(..., alias="documentLayoutData")

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ReferenceLayoutResponse:
    def __init__(
        self,
        prototype_task_result: Optional[TaskResult],
        unifier_task_result: Optional[TaskResult],
        parsing_task_result: Optional[TaskResult],
    ):
        self._prototype_task_result = prototype_task_result
        self._unifier_task_result = unifier_task_result
        self._parsing_task_result = parsing_task_result

        self._validate()

    @cached_property
    def prototype(self) -> Optional[dict]:
        return None if self._prototype_task_result_failed() else self._prototype_task_result  # type: ignore

    @cached_property
    def unified_data(self) -> Optional[dict]:
        return None if self._unifier_task_failed() else json.loads(self._unifier_task_result["content"])  # type: ignore

    @cached_property
    def document_layout_data(self) -> Optional[dict]:
        return None if self._parsing_task_failed() else json.loads(self._parsing_task_result["content"])  # type: ignore

    def make_response(self):
        return ReferenceLayoutResponseData(
            **self.prototype,
            unified_data=self.unified_data,
            document_layout_data=self.document_layout_data,
        ).model_dump(by_alias=True)

    def _validate(self) -> None:
        if self._prototype_task_result_failed():
            raise NotFoundError("Can't find reference layout.")

    def _prototype_task_result_failed(self) -> bool:
        return not self._prototype_task_result or self._is_failed_task(self._prototype_task_result)

    def _unifier_task_failed(self) -> bool:
        return (
            not self._unifier_task_failed
            or self._is_failed_task(self._unifier_task_result)
            or self._is_failed_status_code(self._unifier_task_result["status_code"])  # type: ignore
        )

    def _parsing_task_failed(self) -> bool:
        return (
            not self._parsing_task_result
            or self._is_failed_task(self._parsing_task_result)
            or self._is_failed_status_code(self._parsing_task_result["status_code"])  # type: ignore
        )

    @staticmethod
    def _is_failed_status_code(status_code: int) -> bool:
        return status_code != HTTPStatus.OK

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return issubclass(type(task_result), Exception)
