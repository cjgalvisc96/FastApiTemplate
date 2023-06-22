from fastapi import Depends, APIRouter
from dependency_injector.wiring import inject, Provide
from fastapi.security import SecurityScopes, OAuth2PasswordRequestForm

from backend.container import ApplicationContainer
from backend.users.services.auth import AuthService
from backend.users.utils import GetAuthenticatedUser
from backend.shared import encypt_password, GeneralAPIException
from backend.users.api.validator import CreateUserPayloadValidator
from backend.users.services.users import UsersService, CreateUserDto
from backend.users.api.serializers import TokenSerializer, UserSerlializer

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/token", response_model=TokenSerializer)
@inject
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
):
    try:
        access_token = auth_service.create_access_token(
            email=form_data.username, password=form_data.password, scopes=form_data.scopes
        )
    except Exception as error:
        raise GeneralAPIException(code=400, message=str(error))

    return {"access_token": access_token, "token_type": "bearer"}


@users_router.post("/{user_id}", response_model=UserSerlializer)
@inject
async def create_user(
    user_id: int,
    user: CreateUserPayloadValidator,
    users_service: UsersService = Depends(Provide[ApplicationContainer.users_service]),
):
    input_dto = CreateUserDto(
        id=user_id,
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        password=encypt_password(password=user.password),
    )
    try:
        user_created = users_service.create_user(input_dto=input_dto)
    except Exception as error:
        raise GeneralAPIException(code="test", message=str(error))

    return user_created


@users_router.get(path="/me", response_model=UserSerlializer)
@inject
async def get_my_detail(
    authenticated_user=Depends(
        GetAuthenticatedUser(security_scopes=SecurityScopes(scopes=['users:read']))
    ),
):
    return authenticated_user
