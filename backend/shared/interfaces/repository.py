from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    def create_database(self) -> None:
        ...

    @abstractmethod
    def add(self, entity: T) -> None:
        ...

    @abstractmethod
    def get_all(self) -> list[T]:
        ...

    @abstractmethod
    def get_by_id(self, id: int) -> T | NotFoundError:
        ...

    @abstractmethod
    def update_by_id(self, id: int, data_to_update: dict[str, Any]) -> T | NotFoundError:
        ...

    @abstractmethod
    def remove_by_id(self, id: int) -> T | NotFoundError:
        ...
