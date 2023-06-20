from backend.auctions import AuctionsService


def test_add_batch(mock_uow, mock_logger):
    create_auction_service = AuctionsService(uow=mock_uow, logger=mock_logger)

    create_auction_service.execute(input_dto=None)

    assert mock_uow.batches.get("b1") is not None
    assert mock_uow.committed
