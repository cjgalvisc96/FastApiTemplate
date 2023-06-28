import logging

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient

from backend.app import create_app
from backend.shared import SQLAlchemyDatabase
from backend.container import ApplicationContainer


@pytest.fixture
def app_test():
    container = ApplicationContainer()
    # Override services
    container.db.override(
        providers.Singleton(SQLAlchemyDatabase, db_url=container.config.db.TEST_DB_URL)
    )

    # Simulate FastAPI startup events
    container.db().clean_database()
    container.db().create_database()

    app = create_app(container=container)
    yield app

    container.db().clean_database()


@pytest.fixture
def client(app_test):
    yield TestClient(app=app_test, base_url="http://test")


@pytest.fixture
def caplog(caplog):
    caplog.set_level(logging.INFO)
    yield caplog
    caplog.clear()
