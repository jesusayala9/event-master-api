from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from config.database import SessionLocal
from schemas.user import Users
from services.user import UserService
# from utils.jwt_manager import create_token
from fastapi.responses import  JSONResponse
from schemas.auth import User_Auth
from sqlalchemy.orm import Session
from passlib.context import CryptContext



auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# SECRETKEY = 'MY_Secret_K3y'
# ALGORITHM = 'HS256'

# bcrypt_contest = CryptContext(schemes=['bcrypt'], deprecated='auto')
# oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


# class UserRequest(BaseModel):
#     username: str
#     password: str
    
# class Token (BaseModel):
#     acces_token: str
#     token_type:str

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# db_dependency = Annotated[Session, Depends(get_db)]
# @auth_router.post('/')
# def login_auth(create_user_request: UserRequest, db: Session = Depends(get_db)):
#     create_user_model = Users(
#         username=create_user_request.username,
#         password=bcrypt_contest.hash(create_user_request.password)        
#     )
#     db.add(create_user_model)
#     db.commit()


# @auth_router.post('/login', tags=['auth'])
# def login(user: User_Auth):
#     if user.email == "admin@gmail.com" and user.password == "admin":
#         token: str = create_token(user.model_dump())
#         return JSONResponse(status_code=200, content=token)



# @auth_router.post('/login', tags=['auth'])
# def login(user: User_Auth, db: Session = Depends(get_db)):
#     user_service = UserService(db)
#     user_db = user_service.get_user_by_username(user.username)
#     if user_db and user_service.verify_password(user.password, user_db.password):
#         token: str = create_token({"username": user.username})
#         return JSONResponse(status_code=200, content={"token": token})
#     else:
#         raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    

