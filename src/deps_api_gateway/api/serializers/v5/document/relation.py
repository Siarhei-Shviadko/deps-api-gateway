from ...base import ConfiguredBaseModel

__all__ = ["SerializedRelation"]


class SerializedRelation(ConfiguredBaseModel):
    type: str
    code: str
