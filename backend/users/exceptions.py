class UsersException(Exception):
    ...


class UserDoesNotExist(UsersException):
    ...


class InactiveUser(UsersException):
    ...


class AuthException(Exception):
    ...


class CredentialsIncorrect(AuthException):
    ...


class PermissionsIncorrect(AuthException):
    ...
