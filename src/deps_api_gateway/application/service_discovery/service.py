import json
import logging

from .discoverer import ServiceDiscoverer
from .services_info import ServiceCode, ServiceInfo, ServicesInfo
from .settings import Settings

__all__ = ["ServiceDiscovery"]


class ServiceDiscovery:
    def __init__(self) -> None:
        settings = Settings()

        self._services = json.loads(settings.services)
        self._service_discoverer = ServiceDiscoverer()

        self._logger = logging.getLogger(__class__.__name__)

    def discover(self) -> ServicesInfo:
        self._logger.info("Starting service discovery...")

        deployed_service_names = self._service_discoverer.find_services()

        missed_services: dict[ServiceCode, ServiceInfo] = {}
        deployed_services: dict[ServiceCode, ServiceInfo] = {}

        for service in self._services:
            if service["kubernetes_name"] in deployed_service_names:
                deployed_services[service["code"]] = ServiceInfo(name=service["name"])

            elif service["mandatory"]:
                missed_services[service["code"]] = ServiceInfo(name=service["name"])

        return ServicesInfo(deployed=deployed_services, missed=missed_services)
