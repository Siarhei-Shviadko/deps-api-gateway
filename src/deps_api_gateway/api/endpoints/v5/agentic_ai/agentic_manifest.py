from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response, status

from deps_api_gateway.api.utilities import ResponseBuilder
from deps_api_gateway.application import MetaAgentService
from deps_api_gateway.containers import Application

from ....serializers.v5 import RegisterManifestRequest, RegisterManifestResponse

manifests_router = APIRouter(prefix="/manifests", tags=["Manifests"])


@manifests_router.post("", status_code=status.HTTP_201_CREATED, response_model=RegisterManifestResponse)
@inject
async def register_manifest(
    manifest: RegisterManifestRequest,
    application: MetaAgentService = Depends(Provide[Application.meta_agent]),
) -> Response:
    proxy_response = await application.register_manifest(
        code=manifest.code,
        name=manifest.name,
        description=manifest.description,
        url=manifest.url,
        timeout=manifest.timeout,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@manifests_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_manifests(
    codes: list[str] = Query(
        ..., description="List of manifest codes to delete", alias="code", min_length=1, max_length=100
    ),
    application: MetaAgentService = Depends(Provide[Application.meta_agent]),
) -> Response:
    proxy_response = await application.delete_manifests(
        codes=codes,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
