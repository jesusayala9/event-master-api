from models.event import Event as EventModel
from models.user import Users as UsersModel
from models.user import Users
from schemas.event import Event
from sqlalchemy.orm import Session

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
        result = self.db.query(EventModel).filter(EventModel.title == title).all()
        return result
    
    def get_event_by_category(self, category):
        result = self.db.query(EventModel).filter(EventModel.category == category).all()
        return result
    
    def get_event_by_type(self, type):
        result = self.db.query(EventModel).filter(EventModel.type == type).all()
        return result
    
    # def get_events_by_category_and_title(self, category: str, title: str):
    #     # Buscar eventos por categoría
    #     events_by_category = self.db.query(EventModel).filter(EventModel.category == category).all()
    #     # Buscar eventos por título
    #     events_by_title = self.db.query(EventModel).filter(EventModel.title == title).all()
    #     # Combinar los resultados de ambas consultas
    #     combined_events = events_by_category + events_by_title
    #     # Eliminar duplicados de la lista combinada
    #     unique_events = list(set(combined_events))
    #     return unique_events
    
    def get_events_by_category_and_title_and_type(self, category: str, title: str, event_type: str):
        # Buscar eventos por categoría
        events_by_category = self.db.query(EventModel).filter(EventModel.category.ilike(f"%{category}%")).all()
        # Buscar eventos por título
        events_by_title = self.db.query(EventModel).filter(EventModel.title.ilike(f"%{title}%")).all()
        # Buscar eventos por tipo
        events_by_type = self.db.query(EventModel).filter(EventModel.type.ilike(f"%{event_type}%")).all()
        # Combinar los resultados de las tres consultas
        combined_events = events_by_category + events_by_title + events_by_type
        # Eliminar duplicados de la lista combinada
        unique_events = list(set(combined_events))
        return unique_events
    
    def create_event(self, event:Event):
        new_event = EventModel(**event.model_dump())
        self.db.add(new_event)
        try:
            self.db.commit()
            return True  # Indica que la creación del evento fue exitosa
        except Exception as e:
            self.db.rollback()
            return False 
    
    def update_event(self, id:int, data:Event):
        event = self.db.query(EventModel).filter(EventModel.id == id).first() 
        event.description = data.description
        event.title = data.title
        event.start_time = data.start_time
        event.finish_time = data.finish_time
        event.category = data.category
        event.audience = data.audience
        event.type = data.type
        event.location = data.location
        self.db.commit()
        return    
    
    # def delete_event(self, id:int):
    #     self.db.query(EventModel).filter(EventModel.id == id).delete()      
    #     self.db.commit()
    #     return
    
    def delete_event(self, id: int, db: Session):
        event_to_delete = db.query(EventModel).filter(EventModel.id == id).first()
        if event_to_delete:
            db.delete(event_to_delete)
            db.commit()
            return True
        return False
    
    def get_user_events(self, user_id: int, db: Session):
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            return None
        return user.events

    def get_user_created_events(self, user_id: int, db: Session):        
        user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if not user:
            return None
    # Retorna la lista de eventos creados por el usuario
        return user.created_events

    def get_event_attendees(self, event_id: int, db: Session):
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            return None
        return event.attendees
    
   
    


