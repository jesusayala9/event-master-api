from pydantic import BaseModel


class User_Auth(BaseModel):
    username: str
    password: str