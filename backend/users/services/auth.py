from typing import Any
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from backend.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(
        self,
        *,
        secret_key: str,
        algorithm: str,
        default_token_time_expiration: int,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._default_token_time_expiration = default_token_time_expiration

    @staticmethod
    def verify_password(*, plain_password: str, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(*, password: str) -> str:
        return pwd_context.hash(password)

    def authenticate_user(self, *, user: User, password: str) -> User:
        if not self.verify_password(plain_password=password, hashed_password=user.hashed_password):
            return False
        return user

    def create_access_token(self, *, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self._default_token_time_expiration)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(claims=to_encode, key=self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def decode_payload(self, *, token: str) -> dict[str, Any]:
        return jwt.decode(token=token, key=self._secret_key, algorithms=[self._algorithm])
