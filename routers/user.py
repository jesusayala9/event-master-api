from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from services.event import EventService
from services.user import UserService
from schemas.user import Users
from schemas.user import Users as UsersModel
from schemas.event import Event


user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@user_router.get('/users', tags=['Users'], response_model=list[Users], status_code=200)
def get_users(db: Session = Depends(get_db)) -> list[Users]:
    result = UserService(db).get_users()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@user_router.get('/users/{id}', tags=['Users'], response_model=Users)
def get_user(id: int, db: Session = Depends(get_db)) -> Users:
    result = UserService(db).get_user(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Evento con ID {id} no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@user_router.post('/users', tags=['Users'], response_model=dict, status_code=201)
def create_user(user: Users, db: Session = Depends(get_db)) -> dict:
    try:
        UserService(db).create_user(user)
        return JSONResponse(status_code=201, content={'message': 'Se ha registrado el usuario'})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={'message': 'Error al registrar el usuario'})
    finally:
        db.close()
        # print("Este es el model_dump", user.model_dump())


@user_router.put('/users/{id}', tags=['Users'], response_model=dict, status_code=200)
def update_user(id: int, event: Users, db: Session = Depends(get_db)) -> dict:
    result = UserService(db).get_user(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Evento con ID {id} No encontrado"})
    UserService(db).update_user(id, event)
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado el evento'})


@user_router.delete('/users/{id}', tags=['Users'], response_model=dict, status_code=200)
def delete_user(id: int, db: Session = Depends(get_db)) -> dict:
    user_service = UserService(db)
    if not user_service.delete_user(id):
        return JSONResponse(status_code=404, content={"message": f"Usuario con ID {id} no encontrado"})
    return JSONResponse(status_code=200, content={"message": f"Usuario con ID {id} ha sido eliminado"})



@user_router.get('/users/{id}/events', tags=['Users'])
def get_user_events(id: int, db: Session = Depends(get_db)):
    event_service = EventService(db)
    user_events = event_service.get_user_events(id, db)
    if not user_events:
        return JSONResponse(status_code=404, content={"message": "User not found or has no events."})
    return JSONResponse(status_code=200, content=dict(user_events))


@user_router.get('/users/{id}/events', tags=['Users'])
def get_user_events(id: int, db: Session = Depends(get_db)):
    event_service = EventService(db)
    user_events = event_service.get_user_events(id, db)
    if not user_events:
        return JSONResponse(status_code=404, content={"message": "User not found or has no events."})
    
    # Convertir los eventos en una lista de diccionarios
    user_events_list = []
    for event in user_events:
        user_events_list.append(event.model_dump())
    
    return JSONResponse(status_code=200, content=user_events_list)

@user_router.put("/users/{event_id}/users/{user_id}", tags=["Users"])
def add_user_to_event(event_id: int, user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    event = user_service.add_user_to_event(user_id, event_id)
    if not event:
        return JSONResponse(status_code=404, content={"message": "Usuario o evento no encontrado"})
    return JSONResponse(status_code=200, content={"message": "Usuario añadido al evento correctamente."})
