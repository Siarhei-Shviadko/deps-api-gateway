from deps_api_gateway.constants import (
    V1_PREFIX,
    V2_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)
from deps_api_gateway.domain.dtos import ImportDocumentsData

from .workflow_proxy import IWorkflow

__all__ = ["WorkflowService"]


class WorkflowService:
    def __init__(self, workflow_manager_proxy: IWorkflow) -> None:
        self._workflow_manager_proxy = workflow_manager_proxy

    async def get_saga_state(self, deps_token: str, entity_id: str) -> str:
        return await self._workflow_manager_proxy.get_saga_state(
            url=f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/sagas/{entity_id}/state",
            query="",
            headers={"deps-token": deps_token},
        )

    async def import_documents(
        self,
        deps_token: str,
        data: ImportDocumentsData,
    ) -> None:
        await self._workflow_manager_proxy.import_documents(
            url=f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V2_PREFIX}/import-documents",
            body={
                "paths": data.paths,
                "source": data.source.value,
                "documentType": data.document_type_id,
                "engine": data.engine,
                "language": data.language,
                "invokeUnifier": data.invoke_unifier,
                "invokeExtraction": data.invoke_extraction,
                "parsingFeatures": data.parsing_features,
                "assignedToMe": data.assign_to_me,
            },
            headers={"deps-token": deps_token},
        )
