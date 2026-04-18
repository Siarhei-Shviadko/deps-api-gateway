import json
import logging
from asyncio import Task, create_task
from typing import Any, Coroutine, Optional

from deps_api_gateway.constants import EXTRACTION_TYPE_PLACEHOLDER, DocumentTypeSource
from deps_api_gateway.domain.exceptions import PipelineError

from ...utilities import ParsedRequest
from .pipeline_source import PipelineSource

__all__ = ["GenericPipelineRequest"]


class GenericPipelineRequest:
    DOCUMENT_PIPELINE_URI = ""
    WORKFLOW_PIPELINE_URI = ""

    def __init__(self):
        self.document_pipeline_request: dict[str, Any] = {}  # type: ignore
        self.workflow_manager_pipeline_request: dict[str, Any] = {}  # type: ignore
        self._workflow_request_task = None
        self._document_request_task = None
        self._original_request = None
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def original_request(self) -> ParsedRequest:
        return self._pipeline_request

    @original_request.setter
    def original_request(self, pipeline_request: ParsedRequest) -> None:
        self._pipeline_request = pipeline_request

    @property
    def doc_type_pipeline_mapper(self) -> dict[DocumentTypeSource, PipelineSource]:
        return {
            DocumentTypeSource.CORLEONE: PipelineSource.DOCUMENT,
            DocumentTypeSource.DOCUMENT_TYPE: PipelineSource.WORKFLOW_MANAGER,
        }

    @property
    def pipeline_mapper(self) -> dict[PipelineSource, dict[str, Any]]:
        return {
            PipelineSource.DOCUMENT: self.document_pipeline_request,
            PipelineSource.WORKFLOW_MANAGER: self.workflow_manager_pipeline_request,
        }

    @property
    def workflow_request_task(self):
        return self._workflow_request_task

    @workflow_request_task.setter
    def workflow_request_task(self, coro: Coroutine) -> None:
        self._workflow_request_task = create_task(coro)

    @property
    def document_request_task(self):
        return self._document_request_task

    @document_request_task.setter
    def document_request_task(self, coro: Coroutine) -> None:
        self._document_request_task = create_task(coro)

    def get_pipeline_tasks(self) -> list[Task]:
        tasks = [task for task in (self.workflow_request_task, self.document_request_task) if task is not None]
        if tasks:
            return tasks
        self._logger.error("Pipeline tasks not created.")
        raise PipelineError("No task for running pipeline.")

    async def update_request(self, source: PipelineSource, extraction_type: Optional[str], doc_id: str) -> None:
        if request := self.pipeline_mapper[source]:
            request["data"]["documentIds"].append(doc_id)
            return

        request = await self._create_request(source, extraction_type)
        request["data"]["documentIds"].append(doc_id)

    def serialize_data(self) -> None:
        if req := self.document_pipeline_request or self.workflow_manager_pipeline_request:
            req["data"] = json.dumps(req["data"]).encode()

    async def _create_request(self, source: PipelineSource, extraction_type: str) -> dict[str, Any]:
        request = self.pipeline_mapper[source]

        self._prepare_url(source, extraction_type)
        request.update(await self.original_request.to_dict())
        request["headers"] = self._prepare_headers()
        request["data"] = await self._prepare_data()

        return request

    def _prepare_headers(self) -> dict[str, Any]:
        headers = {}
        headers["deps-token"] = self.original_request.headers["deps-token"]
        headers["content-type"] = self.original_request.headers["content-type"]
        return headers

    def _prepare_url(self, source: PipelineSource, extraction_type: str) -> None:
        url = (
            self.DOCUMENT_PIPELINE_URI
            if source is PipelineSource.DOCUMENT
            else self.WORKFLOW_PIPELINE_URI.replace(EXTRACTION_TYPE_PLACEHOLDER, extraction_type)
        )
        if url != self.original_request.url:
            self.original_request.change_url(self.original_request.url, url)

    async def _prepare_data(self) -> dict[str, Any]:
        data = await self.original_request.json_data
        data["documentIds"] = []
        return data
