from schemas.user import Users
from models.user import Users as UsersModel
from models.event import Event as EventModel
from sqlalchemy.orm import Session
from models.association import association





class UserService():
    def __init__(self, db) -> None:
        self.db = db
        
        
    def get_user_by_username(self, username: str):
        return self.db.query(UsersModel).filter(UsersModel.username == username).first()
    
   

    def get_users(self):
        result = self.db.query(UsersModel).all()
        return result
    
    def get_user(self, id):
        result = self.db.query(UsersModel).filter(UsersModel.id == id).first()
        return result
    
    def create_user(self, user:Users):
        new_user = UsersModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        return  
    
    
    def update_user(self, id:int, data:Users):
            user = self.db.query(UsersModel).filter(UsersModel.id == id).first() 
            user.id = data.id        
            user.username = data.username
            user.email = data.email
            user.password = data.password
            user.events = data.events
            user.created_events = data.created_events
            self.db.commit()
            return
    
    
    def delete_user(self, id: int):
            user_to_delete = self.db.query(UsersModel).filter(UsersModel.id == id).first()
            if user_to_delete:
                self.db.delete(user_to_delete)
                self.db.commit()
                return True
            return False
        
        
  
    
    def add_user_to_event(self, user_id: int, event_id: int):
        user = self.db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if not user:
            return {"message": "Usuario no encontrado"}

        event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            return {"message": "Evento no encontrado"}

        # Verificar si la asociación ya existe usando la tabla de asociación
        existing_association = self.db.query(association).filter_by(user_id=user_id, event_id=event_id).first()
        if existing_association:
            return {"message": "El usuario ya está asociado a este evento"}

        # Asociar el usuario al evento
        user.events.append(event)

        # Incrementar la audiencia del evento
        if event.audience is None:
            event.audience = 1
        else:
            event.audience += 1

        self.db.commit()
        return event


    
    def get_user_events(self, user_id: int):
        user = self.db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if not user:
            return None

        # Serializar eventos creados por el usuario
        created_events = [{
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time.isoformat(),
            "finish_time": event.finish_time.isoformat(),
            "category": event.category,
            "audience": event.audience,
            "type": event.type,
            "location": event.location,
            "attendees": [attendee.id for attendee in event.attendees]
        } for event in user.created_events]

        # Serializar eventos a los que el usuario asistirá
        attending_events = [{
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time.isoformat(),
            "finish_time": event.finish_time.isoformat(),
            "category": event.category,
            "audience": event.audience,
            "type": event.type,
            "location": event.location,
            "attendees": [attendee.id for attendee in event.attendees]
        } for event in user.events]

        # Combinar ambos arrays
        all_events = created_events + attending_events

        # Eliminar duplicados (en caso de que un evento pueda estar en ambas listas)
        unique_events = {event['id']: event for event in all_events}.values()

        return list(unique_events)


    def get_user_created_events(self, user_id: int):
        user = self.db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if not user:
            return None
        return user.created_events
    
    def delete_user_event(self, user_id: int, event_id: int):
        user = self.db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if not user:
            return {"message": "Usuario no encontrado"}
        
        event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            return {"message": "Evento no encontrado"}

        # Si el evento es creado por el usuario, eliminarlo
        if event in user.created_events:
            self.db.delete(event)

        # Si el evento está en la lista de eventos del usuario, desasociarlo
        if event in user.events:
            user.events.remove(event)

        # Guardar los cambios en la base de datos
        self.db.commit()
        return {"message": "Evento eliminado correctamente o usuario desasociado del evento"}
