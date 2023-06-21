from jose import JWTError
from pydantic import ValidationError
from fastapi import status, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi.security import SecurityScopes, OAuth2PasswordBearer

from backend.container import ApplicationContainer
from backend.users import User, AuthService, UsersService, TokenDataSerializer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "users:read": "Read to Users app",
        "users:write": "Write to Users app",
        "auctions:read": "Read to Auctions app",
        "auctions:write": "Write to Auctions app",
    },
)


@inject
async def get_authenticated_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    users_service: UsersService = Depends(Provide[ApplicationContainer.users_service]),
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = auth_service.decode_payload(token=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenDataSerializer(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = users_service.get_user_by_filter(filter_={"email": token_data.username})
    if not user:
        raise credentials_exception

    if not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
