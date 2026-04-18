from typing import Any, Optional, Protocol

from starlette.datastructures import UploadFile

from ..parsing import ParsingFeature
from ..proxy_response import ProxyResponse
from ..types import NeedsReviewOption, Status, WorkflowConfiguration

__all__ = ["IWorkflowManagerProxy"]


class IWorkflowManagerProxy(Protocol):
    async def run_pipeline_from_step(
        self,
        document_ids: list[str],
        step: Status,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        llm_type: Optional[str] = None,
        parsing_features: Optional[set[ParsingFeature]] = None,
    ) -> ProxyResponse:
        ...

    async def create_template(
        self,
        name: str,
        language: str,
        engine: str,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> ProxyResponse:
        ...

    async def create_template_from(
        self,
        src_template_id: str,
        name: str,
        language: str,
        engine: str,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> ProxyResponse:
        ...

    async def create_template_version(
        self,
        document_type_id: str,
        files: list[UploadFile],
        name: str,
        description: Optional[str] = None,
        markup_automatically: bool = False,
    ) -> ProxyResponse:
        ...

    async def upload_document(
        self,
        document_name: str,
        file: UploadFile,
        document_type_id: Optional[str],
        engine: Optional[str],
        language: Optional[str],
        llm_type: Optional[str],
        parsing_features: list[str],
        needs_unifier: bool,
        needs_extraction: bool,
        assign_to_me: bool,
        metadata: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        ...

    async def import_documents(
        self,
        paths: list[str],
        source: str,
        document_type_id: Optional[str],
        engine: Optional[str],
        language: Optional[str],
        llm_type: Optional[str],
        parsing_features: list[str],
        needs_unifier: bool,
        needs_extraction: bool,
        assign_to_me: bool,
        needs_parsing: Optional[bool] = None,
        needs_validation: Optional[bool] = None,
        needs_review: Optional[NeedsReviewOption] = None,
        needs_output_exporting: Optional[bool] = None,
    ) -> ProxyResponse:
        ...

    async def validate_document(self, document_id: str) -> ProxyResponse:
        ...

    async def retry_last_failed_step(self, document_id: str) -> ProxyResponse:
        ...

    async def run_from_first_step(self, document_id: str) -> ProxyResponse:
        ...

    async def complete_review(self, document_id: str) -> ProxyResponse:
        ...

    async def get_saga_state(self, entity_id: str) -> ProxyResponse:
        ...

    async def get_workflow_configuration(self, document_type_id: str) -> ProxyResponse:
        ...

    async def get_workflow_configurations(self) -> ProxyResponse:
        ...

    async def update_workflow_configuration(self, workflow_configuration: WorkflowConfiguration) -> ProxyResponse:
        ...
