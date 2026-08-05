from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response
from fastapi import status as http_status

from deps_api_gateway.application import SplittingService
from deps_api_gateway.constants import SPLITTING_PROPOSALS_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers.v5 import GetProposalResponse, UpdateProposalRequest
from ....utilities import ResponseBuilder

__all__ = ["splitting_proposals_router"]

splitting_proposals_router = APIRouter(prefix=SPLITTING_PROPOSALS_ROUTER_PREFIX, tags=["Splitting"])


@splitting_proposals_router.get(
    "/{proposalId}", status_code=http_status.HTTP_200_OK, response_model=GetProposalResponse
)
@inject
async def get_proposal(
    proposal_id: str = Path(..., alias="proposalId"),
    splitting_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitting_service.get_proposal(proposal_id=proposal_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@splitting_proposals_router.patch("/{proposalId}", status_code=http_status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def update_proposal(
    request: UpdateProposalRequest,
    proposal_id: str = Path(..., alias="proposalId"),
    splitting_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitting_service.update_proposal(
        proposal_id=proposal_id,
        data=request.model_dump(by_alias=True, exclude_none=True),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@splitting_proposals_router.post(
    "/{proposalId}/confirm",
    status_code=http_status.HTTP_202_ACCEPTED,
    response_model=None,
)
@inject
async def confirm_proposal(
    proposal_id: str = Path(..., alias="proposalId"),
    splitting_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitting_service.confirm_proposal(proposal_id=proposal_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
