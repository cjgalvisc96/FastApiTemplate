from fastapi import Depends, Security, APIRouter
from dependency_injector.wiring import inject, Provide
from fastapi.security import SecurityScopes, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.users.models import User
from backend.shared import GeneralAPIException
from backend.container import ApplicationContainer
from backend.users.services.auth import AuthService
from backend.users.api.validator import CreateUserPayloadValidator
from backend.users.exceptions import AuthException, UsersException
from backend.users.services.users import UsersService, CreateUserDto
from backend.users.api.serializers import TokenSerializer, UserSerlializer

users_router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "users:read": "Read to Users app",
        "users:write": "Write to Users app",
    },
)

# TODO: Move this to backend.users.utils.py or backend.shared.auth.py
# is neccesary resolve the 'token: str = Depends(oauth2_scheme)' Dependency

@inject
def get_authenticated_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> User:
    try:
        authenticated_user = auth_service.get_authenticated_user(
            security_scopes=security_scopes, token=token
        )
    except (AuthException, UsersException) as error:
        raise GeneralAPIException(code=400, message=str(error))

    return authenticated_user


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
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
):
    input_dto = CreateUserDto(
        id=user_id,
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        password=auth_service.encypt_password(password=user.password),
    )
    try:
        user_created = users_service.create_user(input_dto=input_dto)
    except Exception as error:
        raise GeneralAPIException(code="test", message=str(error))

    return user_created


@users_router.get("/me", response_model=UserSerlializer)
async def get_my_detail(
    authenticated_user: User = Security(get_authenticated_user, scopes=['users:read'])
):
    return authenticated_user
