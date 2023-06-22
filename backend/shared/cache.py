from fastapi_cache import caches, close_caches, CacheRegistry
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend

from backend.shared import Cache


class FastApiRedisCacheImp(Cache):
    def __init__(self, url: str) -> None:
        self._url = url

    def init_cache(self) -> None:
        rc = RedisCacheBackend(address=self._url)
        caches.set(CACHE_KEY, rc)

    @staticmethod
    def get_cache() -> CacheRegistry:
        return caches.get(CACHE_KEY)

    @staticmethod
    async def close_cache() -> None:
        await close_caches()
