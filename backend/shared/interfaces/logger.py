from abc import ABC, abstractmethod


class ILogger(ABC):
    @abstractmethod
    def debug(self, *, message: str):
        ...

    @abstractmethod
    def error(self, *, message: str):
        ...

    @abstractmethod
    def info(self, *, message: str):
        ...
