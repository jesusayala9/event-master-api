from fastapi import APIRouter
from utils.jwt_manager import create_token
from fastapi.responses import  JSONResponse
from schemas.auth import User_Auth

auth_router = APIRouter()

# class User(BaseModel):
#     email: str
#     password: str


@auth_router.post('/login', tags=['auth'])
def login(user: User_Auth):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)