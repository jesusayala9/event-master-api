from models.event import Event as EventModel
from models.user import Users as UsersModel
from models.user import Users
from schemas.event import Event
from sqlalchemy.orm import Session


def to_dict(self):
    return {
        "username": self.username,
        "email": self.email,
        "password": self.password,
        "events": self.events,
        "created_events": self.created_events,
    }


class EventService():

    def __init__(self, db) -> None:
        self.db = db

    def get_events(self):
        result = self.db.query(EventModel).all()
        
        return result

    def get_event(self, id):
        result = self.db.query(EventModel).filter(EventModel.id == id).first()
        return result

    def get_event_by_title(self, title):
        result = self.db.query(EventModel).filter(
            EventModel.title == title).all()
        return result

    def get_event_by_category(self, category):
        result = self.db.query(EventModel).filter(
            EventModel.category == category).all()
        return result

    def get_event_by_type(self, type):
        result = self.db.query(EventModel).filter(
            EventModel.type == type).all()
        return result

    def get_events_by_category_and_title_and_type(self, category: str, title: str, event_type: str):
        # Buscar eventos por categoría
        events_by_category = self.db.query(EventModel).filter(
            EventModel.category.ilike(f"%{category}%")).all()
        # Buscar eventos por título
        events_by_title = self.db.query(EventModel).filter(
            EventModel.title.ilike(f"%{title}%")).all()
        # Buscar eventos por tipo
        events_by_type = self.db.query(EventModel).filter(
            EventModel.type.ilike(f"%{event_type}%")).all()
        # Combinar los resultados de las tres consultas
        combined_events = events_by_category + events_by_title + events_by_type
        # Eliminar duplicados de la lista combinada
        unique_events = list(set(combined_events))
        return unique_events
    
    def create_event(self, event_data: dict) -> bool:
        try:
            print("Datos recibidos para crear el evento:", event_data)
            new_event = EventModel(**event_data)
            self.db.add(new_event)
            self.db.commit()
            self.db.refresh(new_event)
            print("Evento creado en la base de datos:", new_event)
            return True
        except Exception as e:
            print(f"Error al crear el evento en la base de datos: {e}")
            self.db.rollback()
            return False

    def update_event(self, id: int, data: Event):
        event = self.db.query(EventModel).filter(EventModel.id == id).first()
        event.title = data.title
        event.description = data.description        
        event.start_time = data.start_time
        event.finish_time = data.finish_time
        event.category = data.category        
        event.type = data.type
        event.location = data.location
        event.creator_id = data.creator_id
        self.db.commit()
        return

   
    def delete_event(self, id: int, db: Session):
        event_to_delete = db.query(EventModel).filter(
            EventModel.id == id).first()
        if event_to_delete:
            db.delete(event_to_delete)
            db.commit()
            return True
        return False

    def get_event_attendees(self, event_id: int):
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None
        # Convertir los asistentes en una lista de diccionarios utilizando la función utilitaria
        attendees = [to_dict(attendee) for attendee in event.attendees]
        return attendees
