from abc import ABC, abstractmethod, abstractstaticmethod


class ICache(ABC):
    @abstractmethod
    def init_cache(self) -> None:
        ...

    @abstractstaticmethod
    def get_cache() -> None:
        ...

    @abstractstaticmethod
    async def close_cache() -> None:
        ...
