from ..iproxies import IWorkflowManagerProxy
from ..proxy_response import ProxyResponse
from ..types import WorkflowConfiguration

__all__ = ["WorkflowService"]


class WorkflowService:
    def __init__(self, workflow_manager_proxy: IWorkflowManagerProxy):
        self._workflow_manager_proxy = workflow_manager_proxy

    async def get_saga_state(self, entity_id: str) -> ProxyResponse:
        return await self._workflow_manager_proxy.get_saga_state(entity_id)

    async def get_workflow_configuration(self, document_type_id: str) -> ProxyResponse:
        return await self._workflow_manager_proxy.get_workflow_configuration(document_type_id)

    async def get_workflow_configurations(self) -> ProxyResponse:
        return await self._workflow_manager_proxy.get_workflow_configurations()

    async def update_workflow_configuration(self, workflow_configuration: WorkflowConfiguration) -> ProxyResponse:
        return await self._workflow_manager_proxy.update_workflow_configuration(workflow_configuration)
