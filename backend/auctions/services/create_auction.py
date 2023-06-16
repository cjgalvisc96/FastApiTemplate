from backend.shared import IUnitOfWork
from backend.auctions.unit_of_work import AuctionsUnitOfWork

uow = AuctionsUnitOfWork()

def create_auction(
    *,
    uow: IUnitOfWork,
) -> float:
    with uow:
        added = uow.auctions.add()
    return added 


created_auction= create_auction(uow=uow)