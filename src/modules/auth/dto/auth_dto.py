from pydantic import BaseModel

class UserRegisterDTO(BaseModel):
    name: str
    email: str
    password: str

class UserLoginDTO(BaseModel):
    email: str
    password: str


