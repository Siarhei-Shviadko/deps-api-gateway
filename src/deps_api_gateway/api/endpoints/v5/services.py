from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from deps_api_gateway.application import ServiceDiscovery, ServicesInfo
from deps_api_gateway.containers import Containers

services_router = APIRouter(prefix="/services", tags=["Services Discovery"])


@services_router.get("", response_model=ServicesInfo)
@inject
def get_services(
    service_discovery: ServiceDiscovery = Depends(Provide[Containers.application.service_discovery]),
):
    return service_discovery.discover()
