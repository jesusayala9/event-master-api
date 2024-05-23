from datetime import datetime
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


user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def format_event_dates(events):
    for event in events:
        if isinstance(event.start_time, str):
            event.start_time = datetime.fromisoformat(event.start_time)
        if isinstance(event.finish_time, str):
            event.finish_time = datetime.fromisoformat(event.finish_time)
        event.start_time = event.start_time.isoformat()
        event.finish_time = event.finish_time.isoformat()
        # Construir un diccionario manualmente
        event_dict = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time,
            "finish_time": event.finish_time,
            "category": event.category,
            "audience": event.audience,
            "type": event.type,
            "location": event.location
        }
        # Reemplazar el objeto Event con el diccionario correspondiente
        events[events.index(event)] = event_dict


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


@user_router.get('/users/{id}/created-events', tags=['Users'])
def get_user_created_events(id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    created_events = user_service.get_user_created_events(id)

    if not created_events:
        return JSONResponse(status_code=404, content={"message": f"Usuario con ID {id} no encontrado o no tiene eventos creados."})

    # Convertir los eventos creados en una lista de diccionarios
    created_events_list = []
    for event in created_events:
        event_dict = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time.isoformat(),
            "finish_time": event.finish_time.isoformat(),
            "category": event.category,
            "audience": event.audience,
            "type": event.type,
            "location": event.location,
            "creator_id": event.creator_id,
        }
        created_events_list.append(event_dict)

    return JSONResponse(status_code=200, content=created_events_list)


@user_router.get('/users/{id}/events', tags=['Users'])
def get_user_events(id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user_events = user_service.get_user_events(id)

    if not user_events:
        return JSONResponse(status_code=404, content={"message": f"Usuario con ID {id} no encontrado o no tiene eventos."})

    return JSONResponse(status_code=200, content=user_events)


# @user_router.post('/users', tags=['Users'], response_model=dict, status_code=201)
# def create_user(user: Users, db: Session = Depends(get_db)) -> dict:
#     try:
#         UserService(db).create_user(user)
#         return JSONResponse(status_code=201, content={'message': 'Se ha registrado el usuario'})
#     except Exception as e:
#         db.rollback()
#         return JSONResponse(status_code=500, content={'message': 'Error al registrar el usuario'})
#     finally:
#         db.close()
        # print("Este es el model_dump", user.model_dump())


@user_router.put('/users/{id}', tags=['Users'], response_model=dict, status_code=200)
def update_user(id: int, event: Users, db: Session = Depends(get_db)) -> dict:
    result = UserService(db).get_user(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Evento con ID {id} No encontrado"})
    UserService(db).update_user(id, event)
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado el evento'})


@user_router.put("/users/{event_id}/users/{user_id}", tags=["Users"])
def add_user_to_event(event_id: int, user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    response = user_service.add_user_to_event(user_id, event_id)

    # Verificar si la respuesta es un diccionario y contiene un mensaje de éxito o error
    if isinstance(response, dict) and "message" in response:
        # Si contiene un mensaje, significa que ocurrió un error o el usuario ya está asociado al evento
        return JSONResponse(status_code=400, content={"message": response["message"]})
    else:
        # Si no contiene un mensaje, significa que la operación fue exitosa
        return JSONResponse(status_code=200, content={"message": "Usuario añadido al evento correctamente."})


@user_router.delete('/users/{id}', tags=['Users'], response_model=dict, status_code=200)
def delete_user(id: int, db: Session = Depends(get_db)) -> dict:
    user_service = UserService(db)
    if not user_service.delete_user(id):
        return JSONResponse(status_code=404, content={"message": f"Usuario con ID {id} no encontrado"})
    return JSONResponse(status_code=200, content={"message": f"Usuario con ID {id} ha sido eliminado"})
