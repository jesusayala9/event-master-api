from sqlite3 import IntegrityError
from models.association import association
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
    
    def get_event_by_category(self, category):
        result = self.db.query(EventModel).filter(EventModel.category == category).all()
        return result
    
    def create_event(self, event:Event):
        new_event = EventModel(**event.model_dump())
        self.db.add(new_event)
        self.db.commit()
        return
    
    def update_event(self, id:int, data:Event):
        event = self.db.query(EventModel).filter(EventModel.id == id).first() 
        event.id       
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
    
   
    


