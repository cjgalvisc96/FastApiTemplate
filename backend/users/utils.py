from fastapi import Request
from dependency_injector.wiring import Provide
from fastapi.security import HTTPBearer, SecurityScopes, HTTPAuthorizationCredentials

from backend.users.models import User
from backend.shared import GeneralAPIException
from backend.container import ApplicationContainer
from backend.users.services.auth import AuthService
from backend.users.exceptions import AuthException, UsersException


class GetAuthenticatedUser(HTTPBearer):
    _auth_service: AuthService = Provide[ApplicationContainer.auth_service]

    def __init__(self, security_scopes: SecurityScopes, auto_error: bool = True):
        super(GetAuthenticatedUser, self).__init__(auto_error=auto_error)
        self._security_scopes = security_scopes

    async def __call__(self, request: Request) -> User | GeneralAPIException:
        credentials: HTTPAuthorizationCredentials = await super(
            GetAuthenticatedUser, self
        ).__call__(request)
        try:
            authenticated_user = self._auth_service.get_authenticated_user(
                security_scopes=self._security_scopes, token=credentials.credentials
            )
        except (AuthException, UsersException) as error:
            raise GeneralAPIException(code=400, message=str(error))

        return authenticated_user
