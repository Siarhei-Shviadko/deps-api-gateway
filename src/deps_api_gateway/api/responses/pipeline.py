import json
import logging
from asyncio import Task
from http import HTTPStatus
from typing import Optional

from deps_api_gateway.domain.exceptions import PipelineError

__all__ = ["PipelineResponse"]


class PipelineResponse:
    def __init__(self, document_response: Optional[Task], workflow_response: Optional[Task]):
        self._document_response = document_response
        self._workflow_response = workflow_response
        self._logger = logging.getLogger(self.__class__.__name__)
        self._validate()

    @property
    def content(self) -> bytes:  # noqa: WPS110
        return b""

    def _validate(self) -> None:
        if all(self._is_invalid(task) for task in (self._document_response, self._workflow_response)):
            self._logger.error(
                "Pipeline responses are invalid. Document_request_task: %s, workflow_request_task: %s"
                % (self._document_response, self._workflow_response)
            )
            raise PipelineError(
                self._get_error_message(self._document_response)
                or self._get_error_message(self._workflow_response)
                or "Pipeline error."
            )

    def _is_invalid(self, task: Optional[Task]) -> bool:
        if task is None:
            return True
        elif task.exception():
            self._logger.debug("Task %s finished with exception. %s" % (task, task.exception()))
            return True
        elif self._is_failed_status_code(task.result()["status_code"]):
            self._logger.debug("Task %s finished with unsuccess status_code: %s" % (task, task.result()["status_code"]))
            return True
        return False

    def _is_failed_status_code(self, status_code: int) -> bool:
        return bool(status_code >= HTTPStatus.BAD_REQUEST)

    def _get_error_message(self, task: Task) -> str:
        default = ""

        if task is None:
            return default
        elif task.exception():
            return str(task.exception())
        elif self._is_failed_status_code(task.result()["status_code"]):
            response_content = json.loads(task.result()["content"])
            return response_content.get("message", default)

        return default
