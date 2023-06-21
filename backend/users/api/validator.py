from pydantic import EmailStr, BaseModel


class CreateUserPayloadValidator(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str
