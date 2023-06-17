from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> None:
        ...

    @abstractmethod
    def get_all(self) -> list[T]:
        ...

    @abstractmethod
    def get_by_id(self, id: int) -> T:
        ...

    @abstractmethod
    def update_by_id(self, id: int) -> T:
        ...

    @abstractmethod
    def remove_by_id(self, id: int) -> T:
        ...
