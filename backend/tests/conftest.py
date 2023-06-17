from logging import INFO

import pytest

from backend.tests.mocks import FakeLogger, FakeRepository, FakeUnitOfWork


@pytest.fixture
def mock_repository():
    return FakeRepository()


@pytest.fixture
def mock_uow(mock_repository):
    return FakeUnitOfWork(repository=mock_repository)


@pytest.fixture
def mock_logger():
    return FakeLogger(
        filename="logTest/logsTest.txt",
        name="DomainLoggerTest",
        level=INFO,
        format_="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        date_format="%d-%b-%y %H:%M:%S",
    )
