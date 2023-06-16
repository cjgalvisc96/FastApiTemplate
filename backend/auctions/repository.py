from sqlalchemy.orm.session import Session

from backend.shared import IGenericRepository
from backend.auctions.models import Auction

class AuctionsRepository(IGenericRepository):

    def __init__(self, *, db_session: Session) -> None:
        self._db_session = db_session

    def add(self, *, entity: Auction) -> None:
        self._db_session.add(entity)

    def get_all(self) -> list[Auction]:
        return self._db_session.query(Auction).all()

    def get_by_id(self, *, id: int) -> Auction:
        return self._db_session.query(Auction).filter_by(id=id).first()

