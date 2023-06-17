from backend.auctions import Auction
from backend.shared import IUnitOfWork
from backend.auctions.unit_of_work import AuctionsUnitOfWork

uow = AuctionsUnitOfWork()


def get_all_auctions(*, uow: IUnitOfWork, presenter: None) -> list[Auction]:
    with uow:
        auctions = uow.auctions.get_all()
    return presenter(auctions)


auctions = get_all_auctions(uow=uow)
