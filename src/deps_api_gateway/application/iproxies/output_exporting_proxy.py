from typing import Protocol

from ...domain import ProfileData
from ..proxy_response import ProxyResponse

__all__ = ["IOutputExportingProxy"]


class IOutputExportingProxy(Protocol):
    async def get_outputs(self, document_id: str) -> ProxyResponse:
        ...

    async def get_profiles(self, document_type_id: str) -> ProxyResponse:
        ...

    async def save_profile(self, document_type_id: str, profile: ProfileData) -> ProxyResponse:
        ...

    async def update_profile(self, document_type_id: str, profile_id: str, profile: ProfileData) -> ProxyResponse:
        ...

    async def delete_profile(self, document_type_id: str, profile_id: str) -> ProxyResponse:
        ...

    async def build_output(self, document_id: str, document_type_id: str, profile_id: str) -> ProxyResponse:
        ...

    async def delete_output(self, document_id: str, output_id: str) -> ProxyResponse:
        ...
