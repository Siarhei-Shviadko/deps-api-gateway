from functools import cached_property
from http import HTTPStatus
from typing import Optional, Union

from deps_api_gateway.domain.exceptions import UnifiedDataError

TaskResult = Union[dict, BaseException]


__all__ = ["UnifiedDataRoutedResponse"]


class UnifiedDataRoutedResponse:
    def __init__(self, preprocess_task_result: Optional[TaskResult], unifier_task_result: Optional[TaskResult]):
        self._preprocess_task_result = preprocess_task_result
        self._unifier_task_result = unifier_task_result
        self._validate()
        self._choose_appropriate_response()

    @cached_property
    def preprocess(self) -> Optional[dict]:
        return None if self._preprocess_task_failed() else self._preprocess_task_result  # type: ignore

    @cached_property
    def unifier(self) -> Optional[dict]:
        return None if self._unifier_task_failed() else self._unifier_task_result  # type: ignore

    @cached_property
    def chosen_unified_data_json(self) -> str:
        return self._appropriate_response["content"]

    @property
    def status_code(self) -> HTTPStatus:
        return self._appropriate_response["status_code"]

    def _validate(self) -> None:
        if self._preprocess_task_failed() and self._unifier_task_failed():
            raise UnifiedDataError("Can't get unified data.")

    def _preprocess_task_failed(self) -> bool:
        return not self._preprocess_task_result or self._is_failed_task(self._preprocess_task_result)

    def _unifier_task_failed(self) -> bool:
        return not self._unifier_task_result or self._is_failed_task(self._unifier_task_result)

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return issubclass(type(task_result), Exception)

    def _choose_appropriate_response(self):
        if self.unifier and self.preprocess:
            self._appropriate_response = min(self.unifier, self.preprocess, key=lambda resp: resp["status_code"])
        else:
            self._appropriate_response = self.unifier or self.preprocess
