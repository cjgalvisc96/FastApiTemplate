from backend.auctions import create_auction
from backend.shared import IUnitOfWork, IGenericRepository


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
    def __init__(self):
        self.auctions = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_batch():
    uow = FakeUnitOfWork()
    create_auction("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.committed
