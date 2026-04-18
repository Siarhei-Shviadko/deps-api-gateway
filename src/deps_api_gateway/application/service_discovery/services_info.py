from typing import TypedDict

__all__ = ["ServiceCode", "ServiceInfo", "ServicesInfo"]


ServiceCode = str


class ServiceInfo(TypedDict):
    name: str


class ServicesInfo(TypedDict):
    deployed: dict[ServiceCode, ServiceInfo]
    missed: dict[ServiceCode, ServiceInfo]
