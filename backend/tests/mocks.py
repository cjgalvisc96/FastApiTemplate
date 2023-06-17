from unittest.mock import MagicMock

from backend.auctions import CreateAuctionService
from backend.shared import ILogger, IUnitOfWork, IGenericRepository


class FakeLogger(ILogger):
    def __init__(
        self,
        *,
        filename: str,
        name: str,
        level: str,
        format_: str,
        date_format: str,
    ) -> None:
        super().__init__(
            filename=filename,
            name=name,
            level=level,
            format_=format_,
            date_format=date_format,
        )
        self.debug_mock = MagicMock()
        self.error_mock = MagicMock()
        self.info_mock = MagicMock()

    def debug(self, *, message: str):
        self.debug_mock(message=message)

    def error(self, *, message: str):
        self.error_mock(message=message)

    def info(self, *, message: str):
        self.info_mock(message=message)


class FakeRepository(IGenericRepository):
    def __init__(self, *, auctions):
        self._auctions = set(auctions)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self, *, repository):
        self.repository = repository
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
