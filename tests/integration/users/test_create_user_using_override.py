from unittest.mock import Mock

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient

from backend.app import create_app
from backend.container import ApplicationContainer
from backend.users import User, SQLAlchemyUsersRepositoryImp
from backend.shared import encypt_password, SQLAlchemyDatabase


@pytest.fixture
def app_test():
    container = ApplicationContainer()
    # Override services
    container.db.override(
        providers.Singleton(
            SQLAlchemyDatabase, db_url="mysql://user:password@db:3306/test_app_database"
        )
    )

    # Simulate FastAPI startup events
    container.db().create_database()
    container.fastapi_redis_cache().init_cache()

    app = create_app(container=container)
    yield app

    # Simulate FastAPI shutdown events
    container.fastapi_redis_cache().close_cache()


@pytest.fixture
def client(app_test):
    yield TestClient(app=app_test, base_url="http://test")


def test_token_admin(client):
    authentication_response = client.post(
        url="/v1/users/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "",
            "client_id": "",
            "client_secret": "",
            "username": "admin@gmail.com",
            "password": "admin",
            "scope": "users:all",
        },
    )

    assert authentication_response.status_code == 200
    assert authentication_response.json()['access_token']

    # return authentication_response.json()['access_token']


# def xtest_create_a_valid_user(token_admin, client):
#     repository_mock = Mock(spec=SQLAlchemyUsersRepositoryImp)
#     repository_mock.add.return_value = User(
#         id=1,
#         name="TestName",
#         lastname="TestLastname",
#         email="test@gmail.com",
#         hashed_password=encypt_password(password='TestPassword'),
#         active=True,
#     )
#     with app.container.users_repository.override(repository_mock):
#         users_response = client.post(
#             url="/v1/users/1",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {token_admin}",
#             },
#             json={
#                 "name": "TestName",
#                 "lastname": "TestLastname",
#                 "email": "test@gmail.com",
#                 "password": "TestPassword",
#             },
#         )

#     repository_mock.add.assert_called_once()

#     assert users_response.status_code == 201
#     assert users_response.json() == {
#         "name": "TestName",
#         "lastname": "TestLastname",
#         "email": "test@gmail.com",
#     }
