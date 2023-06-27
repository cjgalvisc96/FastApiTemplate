from pydantic import BaseModel


class TokenSerializer(BaseModel):
    access_token: str
    token_type: str


class TokenDataSerializer(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class UserSerlializer(BaseModel):
    name: str
    lastname: str
    email: str

    class Config:
        orm_mode = True
