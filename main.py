from datetime import datetime
from http.client import HTTPException
from typing import Any, Coroutine,  List, Annotated
from enum import Enum
from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from models.event import Event as EventModel
from config.database import engine, SessionLocal, Base
from fastapi.encoders import jsonable_encoder



app = FastAPI()
app.title = 'EventMaster API'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)


# validar datos del usuario
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)  # obtiene las credenciales del token
        # valida y decodificar y devuelve los datos contenidos.
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(
                status_code=403, detail='Credenciales son invalidas')


class User(BaseModel):
    email: str
    password: str


class EventType(str, Enum):
    presencial = "Presencial"
    virtual = "Virtual"


# datetime(año, mes, dia, hora, min, segundo)

# Se validan los datos con la propiedad Field


class Event(BaseModel):
    id: int
    title: str = Field(default='Nuevo Evento', max_length=20)
    description: str = Field(default='sin Descripcion', max_length=50)
    startTime: datetime = Field(datetime(2024, 1, 4, 10, 0))
    finishTime: datetime = Field(datetime(2024, 1, 4, 11, 0))
    category: str = Field(default='Sin Categoria', max_length=20)
    audience: int = Field(default=0)
    type: EventType = Field(default=EventType.presencial)
    location: str = Field(default='Sin Locacion')

    def model_dump(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "startTime": self.startTime,
            "finishTime": self.finishTime,
            "category": self.category,
            "audience": self.audience,
            'type': self.type,
            'location': self.location
        }

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'Nuevo Evento',
                'description': 'Sin descripcion',
                'startTime': datetime(2024, 1, 4, 10, 0),
                'finishTime': datetime(2024, 1, 4, 11, 0),
                'category': 'students',
                'audience': 0,
                'type': EventType.presencial,
                'location': 'Sin Locacion'
            }
        }


events = [
    {
        'id': 1,
        'title': 'DevFest',
        'description': 'asdasd',
        'startTime': datetime(2024, 1, 4, 10, 0),
        'finishTime': datetime(2024, 1, 4, 11, 0),
        'category': 'tedtalk',
        'audience': 10,
        'type': EventType.presencial,
        'location': 'Tulua'
    },

    {
        'id': 2,
        'title': 'JsConf',
        'description': 'asdasd',
        'startTime': datetime(2024, 1, 4, 10, 0),
        'finishTime': datetime(2024, 1, 4, 11, 0),
        'category': 'students',
        'audience': 20,
        'type': EventType.presencial,
        'location': 'Tulua'
    },
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def format_event_dates(events):
    for event in events:
        if isinstance(event.startTime, str):
            event.startTime = datetime.fromisoformat(event.startTime)
        if isinstance(event.finishTime, str):
            event.finishTime = datetime.fromisoformat(event.finishTime)
        event.startTime = event.startTime.isoformat()
        event.finishTime = event.finishTime.isoformat()
        # Construir un diccionario manualmente
        event_dict = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "startTime": event.startTime,
            "finishTime": event.finishTime,
            "category": event.category,
            "audience": event.audience,
            "type": event.type,
            "location": event.location
        }
        # Reemplazar el objeto Event con el diccionario correspondiente
        events[events.index(event)] = event_dict

# endpoints
# metodos GET


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

# endpoint usuarios


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)


@app.get('/events', tags=['Events'], response_model=list[Event], status_code=200, dependencies=[Depends(JWTBearer())])
def get_events(db: Session = Depends(get_db)) -> list[Event]:
    result = db.query(EventModel).all()
    format_event_dates(result)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.get('/events/{id}', tags=['Events'], response_model=Event)
def get_event(id: int, db: Session = Depends(get_db)) -> Event:
    result = db.query(EventModel).filter(EventModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# si no se especifica el parametro en la direccion, se detecta como parametro query
@app.get('/events/', tags=['Events'], response_model=list[Event])
def get_events_by_Category(category: str = Query(min_length=5, max_length=15), db: Session = Depends(get_db)) -> list[Event]:
    try:
        result = db.query(EventModel).filter(EventModel.category == category).all()
        if not result:
            return JSONResponse(status_code=404, content={'message': 'No se encontraron eventos para la categoría especificada'})
        format_event_dates(result)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})


# def get_events_by_Category(category: str = Query(min_length=5, max_length=15)) -> list[Event]:
#     db = Session()
#     result = db.query(EventModel. category == category).all()       
#     # Formatear fechas en los eventos filtrados
#     format_event_dates(result)
#     return JSONResponse(status_code=200, content=jsonable_encoder(result))


# metodos POST


@app.post('/events', tags=['Events'], response_model=dict, status_code=201)
def create_event(event: Event, db: Session = Depends(get_db)) -> dict:
    try:
        new_event = EventModel(**event.model_dump())
        db.add(new_event)
        db.commit()
        return JSONResponse(status_code=201, content={'message': 'Se ha registrado el evento'})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={'message': 'Error al registrar el evento'})
    finally:
        db.close()

        print("Este es el model_dump", event.model_dump())

# metodo PUT


@app.put('/events/{id}', tags=['Events'], response_model=dict, status_code=200)
def update_Event(id: int, event: Event, db: Session = Depends(get_db)) -> dict:
    result = db.query(EventModel).filter(EventModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Evento con ID {id} No encontrado"})
    result.id = event.id
    result.title = event.title
    result.description = event.description
    result.startTime = event.startTime
    result.finishTime = event.finishTime
    result.category = event.category
    result.audience = event.audience
    result.type = event.type
    result.location = event.location
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado el evento'})   

# metodo DELETE


@app.delete('/events/{id}', tags=['Events'], response_model=dict, status_code=200)
def delete_event(id: int, db: Session = Depends(get_db)) -> dict:
    result = db.query(EventModel).filter(EventModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Evento con ID {id} No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={'message': f'Evento con ID {id} ha sido eliminado'})
    


# @app.post('/events', tags=['Events'], response_model=dict, status_code=201)
# def create_event(event: Event) -> dict:
#     # Convertir el evento a un diccionario y agregarlo a la lista events
#     db_Session = Session()
#     new_event = EventModel(**event.model_dump())
#     db_Session.add(new_event)
#     db_Session.commit()
#     # events.append(event.model_dump())
#     return JSONResponse(status_code=201, content={'message': 'Se ha registrado el evento'})
