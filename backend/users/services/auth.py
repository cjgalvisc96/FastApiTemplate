from typing import Any
from datetime import datetime, timedelta

from jose import jwt
from pydantic import BaseModel

from backend.users.models import User
from backend.shared import pwd_context
from backend.users.exceptions import (
    InactiveUser,
    TokenMalformed,
    UserDoesNotExist,
    CredentialsIncorrect,
    PermissionsIncorrect,
)


class TokenDataSerializer(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class AuthService:
    def __init__(
        self,
        *,
        secret_key: str,
        algorithm: str,
        default_token_time_expiration: int,
        users_repository,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._default_token_time_expiration = default_token_time_expiration
        self._users_repository = users_repository

    def _decode_token_payload(self, *, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token=token, key=self._secret_key, algorithms=[self._algorithm])
        except Exception:
            raise TokenMalformed("Token malformed")

    def create_access_token(self, *, email, password, scopes) -> str:
        user = self._users_repository.get_by_filter(filter_={'email': email})
        if not user:
            raise UserDoesNotExist("User does not exists")

        if not pwd_context.verify(secret=password, hash=user.hashed_password):
            raise CredentialsIncorrect("Password incorrect")

        to_encode = {"sub": user.email, "scopes": scopes}
        expire = datetime.utcnow() + timedelta(minutes=self._default_token_time_expiration)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(claims=to_encode, key=self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def get_authenticated_user(self, security_scopes, token) -> User:
        payload = self._decode_token_payload(token=token)

        username: str = payload.get("sub")
        if username is None:
            raise CredentialsIncorrect("Could not validate credentials")

        token_scopes = payload.get("scopes", [])
        token_data = TokenDataSerializer(scopes=token_scopes, username=username)

        user = self._users_repository.get_by_filter(filter_={"email": token_data.username})
        if not user:
            raise CredentialsIncorrect("Could not validate credentials")

        if not user.active:
            raise InactiveUser("Inactive user")

        security_scopes = security_scopes.scopes

        if not security_scopes:
            return user

        if not self.check_scopes(security_scopes=security_scopes, user_scopes=token_data.scopes):
            raise PermissionsIncorrect("Not enough permissions")

        return user

    @staticmethod
    def check_scopes(*, security_scopes: list[str], user_scopes: list[str]) -> bool:
        return False if not set(security_scopes).intersection(set(user_scopes)) else True
