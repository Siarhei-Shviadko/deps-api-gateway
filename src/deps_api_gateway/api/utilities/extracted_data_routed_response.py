from functools import cached_property
from http import HTTPStatus
from typing import Optional, Union

from deps_api_gateway.domain.exceptions import ExtractedDataError

TaskResult = Union[dict, BaseException]

__all__ = ["ExtractedDataRoutedResponse"]


class ExtractedDataRoutedResponse:
    def __init__(self, corleone_task_result: Optional[TaskResult], extraction_task_result: Optional[TaskResult]):
        self._corleone_task_result = corleone_task_result
        self._extraction_task_result = extraction_task_result
        self._validate()
        self._choose_appropriate_response()

    @cached_property
    def corleone(self) -> Optional[dict]:
        return None if self._corleone_task_failed() else self._corleone_task_result  # type: ignore

    @cached_property
    def extraction(self) -> Optional[dict]:
        return None if self._extraction_task_failed() else self._extraction_task_result  # type: ignore

    @cached_property
    def chosen_extracted_data_json(self) -> str:
        return self._appropriate_response["content"]

    @property
    def status_code(self) -> HTTPStatus:
        return self._appropriate_response["status_code"]

    def _validate(self) -> None:
        if self._extraction_task_failed() and self._corleone_task_failed():
            raise ExtractedDataError("Can't get extracted data.")

    def _corleone_task_failed(self) -> bool:
        return not self._corleone_task_result or self._is_failed_task(self._corleone_task_result)

    def _extraction_task_failed(self) -> bool:
        return not self._extraction_task_result or self._is_failed_task(self._extraction_task_result)

    @staticmethod
    def _is_failed_task(task_result: TaskResult) -> bool:
        return issubclass(type(task_result), Exception)

    def _choose_appropriate_response(self) -> None:
        if self.corleone and self.extraction:
            self._appropriate_response = min(self.extraction, self.corleone, key=lambda resp: resp["status_code"])
        else:
            self._appropriate_response = self.extraction or self.corleone
