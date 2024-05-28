from fastapi import APIRouter
from datetime import datetime
from typing import Annotated
from fastapi import Depends,  Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.event import Event as EventModel
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from models.user import Users
from services.auth import get_current_user
from services.event import EventService
from schemas.event import Event, EventResponse


event_router = APIRouter()


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
            "location": event.location,
            "creator_id": event.creator_id
        }
        # Reemplazar el objeto Event con el diccionario correspondiente
        events[events.index(event)] = event_dict

#
@event_router.get('/events', tags=['Events'], response_model=list[Event], status_code=200 )
def get_events(db: Session = Depends(get_db)) -> list[Event]:
    result = EventService(db).get_events()
    format_event_dates(result)    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@event_router.get('/events/{id}', tags=['Events'], response_model=Event)
def get_event(id: int, db: Session = Depends(get_db)) -> Event:
    result = EventService(db).get_event(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Evento con ID {id} no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# si no se especifica el parametro en la direccion, se detecta como parametro query
@event_router.get('/events/', tags=['Events'], response_model=list[Event])
def get_events_by_Category(category: str = Query(min_length=5, max_length=15), db: Session = Depends(get_db)) -> list[Event]:
    try:
        result = EventService(db).get_event_by_category(category)
        if not result:
            return JSONResponse(status_code=404, content={'message': 'No se encontraron eventos para la categoría especificada'})
        format_event_dates(result)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})
    
@event_router.get('/events/by-title/', tags=['Events'], response_model=list[Event])
def get_events_by_title(title: str = Query(..., min_length=1), db: Session = Depends(get_db)) -> list[Event]:
    try:
        result = EventService(db).get_event_by_title(title)
        if not result:
            return JSONResponse(status_code=404, content={'message': 'No se encontraron eventos con el título especificado'})
        format_event_dates(result)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})
    


@event_router.get('/events/search/', tags=['Events'], response_model=list[Event])
def search_events(Title_or_Category_or_Type: str = Query(...), db: Session = Depends(get_db)):
    # Verificar si el parámetro es una categoría, un título de evento o un tipo de evento
    events = EventService(db).get_events_by_category_and_title_and_type(Title_or_Category_or_Type, Title_or_Category_or_Type, Title_or_Category_or_Type)
    if events:
        return events
    else:
        return JSONResponse(status_code=404, content={'message': f"No se encontraron eventos para '{Title_or_Category_or_Type}'"})
    

# metodo POST
@event_router.post('/events', tags=['Events'], response_model=EventResponse, status_code=201)
def create_event(event: Event, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    try:
        print("Datos recibidos para crear el evento:", event.model_dump())
        
        creator_id = current_user.id
        event_data = event.model_dump()
        event_data['creator_id'] = creator_id
        print("Datos del evento a registrar:", event_data)

        success = EventService(db).create_event(event_data)
        
        if success:
            print("Evento registrado con éxito")
            return JSONResponse(status_code=201, content={'message': 'Se ha registrado el evento'})
        else:
            print("Error al registrar el evento en la capa de servicio")
            return JSONResponse(status_code=500, content={'message': 'Error al registrar el evento'})
    except Exception as e:
        print(f"Error en el endpoint al registrar el evento: {e}")
        return JSONResponse(status_code=500, content={'message': f'Error al registrar el evento: {str(e)}'})



# metodo PUT


@event_router.put('/events/{id}', tags=['Events'], response_model=dict, status_code=200)
def update_Event(id: int, event: Event, db: Session = Depends(get_db)) -> dict:
    result = EventService(db).get_event(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Evento con ID {id} No encontrado"})
    EventService(db).update_event(id, event)
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado el evento'})

# metodo DELETE


@event_router.delete('/events/{id}', tags=['Events'], response_model=dict, status_code=200)
def delete_event(id: int, db: Session = Depends(get_db)) -> JSONResponse:
    result = db.query(EventModel).filter(EventModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': f"Eventos con ID {id} No encontrado"})
    EventService(db).delete_event(id, db)  # Asegúrate de pasar 'db' aquí
    return JSONResponse(status_code=200, content={'message': f'Evento con ID {id} ha sido eliminado'})

@event_router.get('/events/{id}/attendees', tags=['Events'])
def get_event_attendees(id: int, db: Session = Depends(get_db)):
    event_service = EventService(db)
    event_attendees = event_service.get_event_attendees(id)
    if not event_attendees:
        return JSONResponse(status_code=404, content={"message": "Evento no encontrado o no tiene asistentes"})
    return JSONResponse(status_code=200, content=jsonable_encoder(event_attendees))


