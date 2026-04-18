from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import AttachExtractorRequest
from ....utilities import ResponseBuilder

__all__ = ["extractors_router"]

extractors_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Document Types"])


@extractors_router.post(
    "/attach-extractor",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    description="Find or create a document type by name and attach an extractor to it.\n"
    "Can only attach Plugin and Non type extractors.",
)
@inject
async def attach_extractor(
    attach_extractor_request: AttachExtractorRequest,
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.attach_extractor(
        name=attach_extractor_request.name,
        extractor_type=attach_extractor_request.extractor_type,
        description=attach_extractor_request.description,
        engine=attach_extractor_request.engine,
        language=attach_extractor_request.language,
        image_transformations=attach_extractor_request.image_transformations,
        fields=attach_extractor_request.fields,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extractors_router.delete(
    "/{documentTypeId}/extractors/{extractorId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    description="Detach extractor from document type.\nCan only detach LLM type of extractors.",
)
@inject
async def detach_extractor(
    document_type_id: str = Path(..., alias="documentTypeId"),
    extractor_id: str = Path(..., alias="extractorId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.detach_extractor(document_type_id=document_type_id, extractor_id=extractor_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
