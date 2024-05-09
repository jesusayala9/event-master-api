from typing import List
from pydantic import BaseModel, Field
from schemas.event import Event

class Users(BaseModel):
    id: int
    username: str = Field(default='jhon', max_length=20)
    email: str = Field(default='jhon@mail.com', max_length=20)
    password: str = Field(default='12345@', max_length=20)
    events: List[Event] = []
    created_events: List[Event] = []
 

    def model_dump(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "events": self.events,
            "created_events": self.created_events,           
        }

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'username': 'name',
                'email': 'email@gmail.com',                
                'password': '123456',
                'events': ['evento1', 'evento2'],
                'created_events': ['evento3', 'evento4']
            }
        }