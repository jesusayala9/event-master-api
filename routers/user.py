from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends 
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.user import UserService
from schemas.user import User

user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@user_router.get('/users', tags=['Users'], response_model=list[User], status_code=200, )
def get_users(db: Session = Depends(get_db)) -> list[User]:
    result = UserService(db).get_users()    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@user_router.post('/users', tags=['Users'], response_model=dict, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)) -> dict:
    try:
        UserService(db).create_user(user)
        return JSONResponse(status_code=201, content={'message': 'Se ha registrado el usuario'})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={'message': 'Error al registrar el usuario'})
    finally:
        db.close()
        print("Este es el model_dump", user.model_dump())