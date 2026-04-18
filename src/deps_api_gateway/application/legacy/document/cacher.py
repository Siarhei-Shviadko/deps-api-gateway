from enum import Enum, auto
from typing import Any

from cachetools import TTLCache

__all__ = ["Cacher", "CacheTypes", "RareCacheKeys"]


class RareCacheKeys(Enum):
    LANGUAGES = "languages"
    ENGINES = "engines"
    STATES = "states"


class CacheTypes(Enum):
    RARE = auto()
    DOC_TYPE_SOURCE = auto()
    DOC_TYPE_CODE = auto()
    DOC_TYPE_EXTRACTION = auto()


class Cacher:
    def __init__(
        self,
        rare_cache: TTLCache,
        doc_type_source_cache: TTLCache,
        doc_type_code_cache: TTLCache,
        doc_type_extraction_cache: TTLCache,
    ):
        self._rare_cache = rare_cache
        self._doc_type_source_cache = doc_type_source_cache
        self._doc_type_code_cache = doc_type_code_cache
        self._doc_type_extraction_cache = doc_type_extraction_cache
        self._cache_mapping: dict[CacheTypes, TTLCache] = {
            CacheTypes.RARE: self._rare_cache,
            CacheTypes.DOC_TYPE_EXTRACTION: self._doc_type_extraction_cache,
            CacheTypes.DOC_TYPE_CODE: self._doc_type_code_cache,
            CacheTypes.DOC_TYPE_SOURCE: self._doc_type_source_cache,
        }

    async def cache(self, cache_type: CacheTypes, key: str, value: Any) -> None:
        if self._cache_mapping[cache_type].get(key) == value:
            return
        self._cache_mapping[cache_type][key] = value

    async def get(self, cache_type: CacheTypes, key: str) -> Any:
        return self._cache_mapping[cache_type].get(key)
