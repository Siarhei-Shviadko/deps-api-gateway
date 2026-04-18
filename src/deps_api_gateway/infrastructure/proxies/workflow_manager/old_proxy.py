import json
from http import HTTPStatus
from typing import Any, Optional

from aiohttp import FormData
from async_rest_client import Methods
from starlette.datastructures import UploadFile

from deps_api_gateway.application.legacy import IWorkflow
from deps_api_gateway.constants import V2_PREFIX, WORKFLOW_MANAGER_BASE_API_PREFIX
from deps_api_gateway.domain.exceptions import UploadDocumentError, WorkflowManagerError

from ..form_data import FormDataBuilder
from ..generic_rest_client import OldGenericRestClient

__all__ = ["OldWorkflowManagerProxy"]

FILE_FIELD_NAME: str = "file"
DEPS_TOKEN_KEY: str = "deps-token"


class OldWorkflowManagerProxy(OldGenericRestClient, IWorkflow):
    async def upload_document(
        self,
        url: str,
        form: dict[str, Any],
        file: Optional[UploadFile],
        headers: dict[str, Any],
    ) -> dict:
        request_data = {
            "documentType": form.get("documentType"),
            "documentName": form.get("documentName"),
            "engine": form.get("engine"),
            "language": form.get("language"),
            "llm_type": form.get("llmType"),
            "invokeUnifier": form.get("runPipeline"),
            "invokeExtraction": form.get("extractData"),
            "assignedToMe": form.get("assignedToMe"),
            "metadata": form.get("metadata"),
        }

        form_data = FormData({key: value for key, value in request_data.items() if value is not None})
        if file is not None:
            form_data.add_field(
                FILE_FIELD_NAME,
                await file.read(),
                filename=file.filename,
                content_type=file.content_type,
            )

        headers = {"accept": "application/json", DEPS_TOKEN_KEY: headers.get(DEPS_TOKEN_KEY)}

        async with self._client.post(
            url=url,
            headers=headers,
            data=form_data,
        ) as response:
            if response.status != HTTPStatus.CREATED:
                raise UploadDocumentError(f"Can't upload document. Reason: {await response.read()}")

            return {
                "content": await response.read(),
                "status_code": response.status,
                "headers": response.headers,
            }

    async def upload_document_v2(self, form: dict[str, Any], headers: dict[str, Any]) -> dict:
        url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V2_PREFIX}/upload-document"
        file = form[FILE_FIELD_NAME]

        request_data = {
            "documentName": form.get("documentName"),
            "documentType": form.get("documentType"),
            "engine": form.get("engine"),
            "language": form.get("language"),
            "llm_type": form.get("llmType"),
            "needsUnifier": form.get("runPipeline"),
            "needsExtraction": form.get("extractData"),
            "assignedToMe": form.get("assignedToMe"),
            "metadata": json.dumps(metadata) if (metadata := form.get("metadata")) else None,
        }
        data = {key: value for key, value in request_data.items() if value is not None}

        form_data = (
            FormDataBuilder(data)
            .with_header(key=DEPS_TOKEN_KEY, value=headers.get(DEPS_TOKEN_KEY))
            .with_file(field_name=FILE_FIELD_NAME, filename=file.filename, content=await file.read())
            .build()
        )

        async with self._client.post(
            url=url,
            data=form_data.data,
            headers=form_data.headers,
        ) as response:
            if response.status != HTTPStatus.CREATED:
                raise UploadDocumentError(f"Can't upload document. Reason: {await response.read()}")

            return {
                "content": await response.read(),
                "status_code": response.status,
                "headers": response.headers,
            }

    async def import_documents(
        self,
        url: str,
        body: dict[str, Any],
        headers: dict[str, Any],
    ) -> None:
        headers = {"accept": "application/json", "deps-token": headers.get("deps-token")}

        async with self._client.post(
            url=url,
            headers=headers,
            json=body,
        ) as response:
            if response.status != HTTPStatus.OK:
                raise UploadDocumentError("Can't import documents")

    async def get_saga_state(self, url: str, query: str, headers: dict[str, Any]) -> str:
        response = await self.request(Methods.GET, url, query, headers, data=b"")

        if response["status_code"] != HTTPStatus.OK:
            raise WorkflowManagerError("Can't get version markup state!")

        return json.loads(response["content"])
