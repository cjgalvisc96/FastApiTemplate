from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, Security, APIRouter, HTTPException

from backend.shared import GeneralAPIException
from backend.container import ApplicationContainer
from backend.users.utils import get_authenticated_user
from backend.users import (
    AuthService,
    UsersService,
    CreateUserDto,
    TokenSerializer,
    UserSerlializer,
    CreateUserPayloadValidator,
)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/token", response_model=TokenSerializer)
@inject
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users_service: UsersService = Depends(Provide[ApplicationContainer.users_service]),
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
):
    user = users_service.get_user_by_filter(filter_={'email': form_data.username})
    if not user:
        raise HTTPException(status_code=404, detail=f"User={form_data.username} does not exists")

    user_athenticated = auth_service.authenticate_user(user=user, password=form_data.password)
    if not user_athenticated:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth_service.create_access_token(
        data={"sub": user.email, "scopes": form_data.scopes},
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.post("/{user_id}", response_model=UserSerlializer)
@inject
async def create_user(
    user_id: int,
    user: CreateUserPayloadValidator,
    users_service: UsersService = Depends(Provide[ApplicationContainer.users_service]),
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
):
    input_dto = CreateUserDto(
        id=user_id,
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        password=auth_service.get_password_hash(password=user.password),
    )
    try:
        user_created = users_service.create_user(input_dto=input_dto)
    except Exception as error:
        raise GeneralAPIException(code="test", message=str(error))

    return user_created


@users_router.get("/me", response_model=UserSerlializer)
async def get_my_detail(authenticated_user=Security(dependency=get_authenticated_user, scopes=["users:read"])):
    return authenticated_user
