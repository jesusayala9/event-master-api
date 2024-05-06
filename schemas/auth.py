from pydantic import BaseModel


class User_Auth(BaseModel):
    email: str
    password: str