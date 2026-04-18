from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import AddCommendRequest, SerializedComment
from ....utilities import ResponseBuilder

comments_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@comments_router.post("/{documentId}/comments", response_model=SerializedComment, status_code=status.HTTP_200_OK)
@inject
async def add_comment(
    comment_data: AddCommendRequest,
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.add_comment(document_id=document_id, text=comment_data.text)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
