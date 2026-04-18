from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IPrompter
from deps_api_gateway.constants import PROMPTER_BASE_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import PrompterError

__all__ = ["PrompterProxy"]


class PrompterProxy(GenericRestClient, IPrompter):
    exception = PrompterError
    v1_prefix = f"{PROMPTER_BASE_PREFIX}{V1_PREFIX}"

    async def get_llms_with_codes(self) -> dict[str, Any]:
        url = f"{self.v1_prefix}/extraction/models"

        try:
            return await self.request(method=Methods.GET, url=url)
        except Exception as error:
            raise self.exception(error)
