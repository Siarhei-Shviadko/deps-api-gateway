from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from deps_api_gateway.application import WorkflowService
from deps_api_gateway.application.types import WorkflowConfiguration
from deps_api_gateway.containers import Application

from ....serializers import (
    UpdateWorkflowConfigurationRequest,
    WorkflowConfigurationResponse,
)
from ....utilities import ResponseBuilder

__all__ = ["workflow_configuration_router"]

workflow_configuration_router = APIRouter(prefix="/workflow-configuration", tags=["Workflow Manager"])


@workflow_configuration_router.get("/{documentTypeId}", response_model=WorkflowConfigurationResponse)
@inject
async def get_workflow_configuration(
    document_type_id: str = Path(..., alias="documentTypeId"),
    workflow_service: WorkflowService = Depends(Provide[Application.workflow]),
):
    proxy_response = await workflow_service.get_workflow_configuration(document_type_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@workflow_configuration_router.get("", response_model=dict[str, WorkflowConfigurationResponse])
@inject
async def get_workflow_configurations(
    workflow_service: WorkflowService = Depends(Provide[Application.workflow]),
):
    proxy_response = await workflow_service.get_workflow_configurations()
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@workflow_configuration_router.patch("/{documentTypeId}", response_model=WorkflowConfigurationResponse)
@inject
async def update_workflow_configuration(
    workflow_configuration: UpdateWorkflowConfigurationRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    workflow_service: WorkflowService = Depends(Provide[Application.workflow]),
):
    configuration = WorkflowConfiguration(
        document_type_id=document_type_id,
        parsing_features=list(workflow_configuration.parsing_features)
        if workflow_configuration.parsing_features
        else None,
        needs_postprocessing=workflow_configuration.needs_postprocessing,
        needs_extraction=workflow_configuration.needs_extraction,
        needs_validation=workflow_configuration.needs_validation,
        needs_review=workflow_configuration.needs_review,
        needs_output_exporting=workflow_configuration.needs_output_exporting,
        engine=workflow_configuration.engine,
    )
    proxy_response = await workflow_service.update_workflow_configuration(configuration)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
