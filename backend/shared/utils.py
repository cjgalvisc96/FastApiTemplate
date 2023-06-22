from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encypt_password(*, password: str) -> str:
    return pwd_context.hash(password)
