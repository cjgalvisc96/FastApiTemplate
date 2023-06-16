from typing import Self
from abc import ABC, abstractmethod
from backend.shared import IGenericRepository


class IUnitOfWork(ABC):

    entities: IGenericRepository

    @abstractmethod
    def __enter__(self) -> Self:
        ...

    @abstractmethod
    def __exit__(self, *args) -> None:
        ...

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...