from typing import Self
from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
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
