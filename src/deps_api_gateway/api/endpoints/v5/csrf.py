from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_csrf_protect import CsrfProtect

from deps_api_gateway.api.serializers.v5.csrf import CSRFTokenResponseModel
from deps_api_gateway.containers import Containers

csrf_router = APIRouter(prefix="/csrf", tags=["CSRF"])


@csrf_router.get("", response_model=CSRFTokenResponseModel)
@inject
def get_csrf_token(
    csrf_protect: CsrfProtect = Depends(), secret_key: str = Depends(Provide[Containers.config.csrf.secret_key])
):
    token, _ = csrf_protect.generate_csrf_tokens(secret_key=secret_key)
    return CSRFTokenResponseModel(token=token)
