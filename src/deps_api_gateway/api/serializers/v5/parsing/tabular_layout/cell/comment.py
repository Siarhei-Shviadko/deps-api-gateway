from deps_api_gateway.api.serializers import ConfiguredBaseModel

__all__ = ["SerializedComment"]


class SerializedComment(ConfiguredBaseModel):
    author: str
    content: str
