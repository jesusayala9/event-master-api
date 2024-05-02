from datetime import datetime
from http.client import HTTPException
from typing import Any, Coroutine,  List
from enum import Enum
from fastapi import Depends, FastAPI, Body, Path, Query, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
# from config.database import Session, engine, Base
# from models.event import Event


app = FastAPI()
app.title = 'EventMaster API'
app.version = '0.0.1'

# Base.metadata.create_all(bind=engine)


# validar datos del usuario
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)# obtiene las credenciales del token
        data = validate_token(auth.credentials)# valida y decodificar y devuelve los datos contenidos.
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code= 403, detail='Credenciales son invalidas')


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


# def format_event_dates(events):
#     for item in events:
#         if isinstance(item['startTime'], str):
#             item['startTime'] = datetime.fromisoformat(item['startTime'])
#         if isinstance(item['finishDate'], str):
#             item['finishTime'] = datetime.fromisoformat(item['finishTime'])
#         item['startTime'] = item['startTime'].isoformat()
#         item['finishTime'] = item['finishTime'].isoformat()


def format_event_dates(events):
    for item in events:
        if isinstance(item['startTime'], str):
            item['startTime'] = datetime.fromisoformat(item['startTime'])        
        if isinstance(item['finishTime'], str):
            item['finishTime'] = datetime.fromisoformat(item['finishTime'])
        item['startTime'] = item['startTime'].isoformat()
        item['finishTime'] = item['finishTime'].isoformat()

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
def get_events() -> list[Event]:
    response = events
    format_event_dates(response)
    return JSONResponse(status_code=200, content=response)


@app.get('/events/{id}', tags=['Events'], response_model=Event)
def get_event(id: int) -> Event:
    for item in events:
        if item['id'] == id:
            # Copia el diccionario para evitar modificaciones en el original
            response = [item.copy()]
            format_event_dates(response)
            return JSONResponse(content=response)
    return JSONResponse(status_code=404, content=[])


# si no se especifica el parametro en la direccion, se detecta como parametro query
@app.get('/events/', tags=['Events'], response_model=list[Event])
def get_events_by_Category(category: str) -> list[Event]:
    filtered_events = [item for item in events if item['category'] == category]
    # Formatear fechas en los eventos filtrados
    format_event_dates(filtered_events)
    return JSONResponse(content=filtered_events)


# metodos POST


@app.post('/events', tags=['Events'], response_model=dict, status_code=201)
def create_event(event: Event) -> dict:
    # Convertir el evento a un diccionario y agregarlo a la lista events
    events.append(event.model_dump())
    return JSONResponse(status_code=201, content={'message': 'Se ha registrado el evento'})

# metodo PUT


# @app.put('/events/{id}', tags=['Events'])
# def uptdate_Event(id: int, event: Event):
#     for item in events:
#         if item['id'] == id:
#             item['title'] = event.title
#             item['description'] = event.description
#             item['startTime'] = event.startTime
#             item['finisTime'] = event.finishTime
#             item['category'] = event.category
#             item['audience'] = event.audience
#             item['type'] = event.type
#             item['location'] = event.location
#             return JSONResponse(content={'message':'Se ha modificado el evento'})


@app.put('/events/{id}', tags=['Events'], response_model=dict, status_code=200)
def update_Event(id: int, event: Event) -> dict:
    for item in events:
        if item['id'] == id:
            # Actualizar los atributos del evento con los valores del objeto Event recibido
            item['id'] = event.id
            item['title'] = event.title
            item['description'] = event.description
            item['startTime'] = event.startTime           
            item['finishTime'] = event.finishTime
            item['category'] = event.category
            item['audience'] = event.audience
            item['type'] = event.type
            item['location'] = event.location
            return JSONResponse(status_code=200, content={'message': 'Se ha modificado el evento'})
    # Si no se encuentra ningún evento con el ID especificado, devolver un mensaje de error
    return JSONResponse(status_code=404, content={'message': 'Evento con ID {id} no encontrado'})

# metodo DELETE


@app.delete('/events/{id}', tags=['Events'], response_model=dict, status_code=200)
def delete_event(id: int) -> dict:
    for item in events:
        if item['id'] == id:
            events.remove(item)
            return JSONResponse(status_code=200, content={'message': f'Evento con ID {id} ha sido eliminado'})
    # Si no se encuentra ningún evento con el ID especificado, devolver un mensaje de error
    return JSONResponse(status_code=404, content={'message': f'No se encontró ningún evento con el ID {id}'})


# @app.delete('/events/{id}', tags=['Events'])
# def delete_event(id: int):
#     for item in events:
#         if item['id'] == id:
#             events.remove(item)
#             return events
