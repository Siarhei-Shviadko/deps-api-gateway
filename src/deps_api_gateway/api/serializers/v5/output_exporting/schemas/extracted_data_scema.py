from ....base import ConfiguredBaseModel

__all__ = ["ExtractedDataSchema"]


class ExtractedDataSchema(ConfiguredBaseModel):
    fields: list[str]
    needs_validation_results: bool
