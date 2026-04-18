from .new import GenericRestClient
from .old import OldGenericRestClient

__all__ = new.__all__ + old.__all__
