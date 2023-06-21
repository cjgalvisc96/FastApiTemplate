from dataclasses import dataclass


@dataclass
class User:
    name: str
    lastname: str
    email: str
    hashed_password: str
    active: bool = True
