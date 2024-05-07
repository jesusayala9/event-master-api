from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from config.database import SessionLocal
from services.user import UserService
from utils.jwt_manager import create_token
from fastapi.responses import  JSONResponse
from schemas.auth import User_Auth
from sqlalchemy.orm import Session
from passlib.context import CryptContext



auth_router = APIRouter()




# class User(BaseModel):
#     email: str
#     password: str


# @auth_router.post('/login', tags=['auth'])
# def login(user: User_Auth):
#     if user.email == "admin@gmail.com" and user.password == "admin":
#         token: str = create_token(user.model_dump())
#         return JSONResponse(status_code=200, content=token)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@auth_router.post('/login', tags=['auth'])
def login(user: User_Auth, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user_db = user_service.get_user_by_username(user.username)
    if user_db and user_service.verify_password(user.password, user_db.password):
        token: str = create_token({"username": user.username})
        return JSONResponse(status_code=200, content={"token": token})
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    

