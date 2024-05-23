from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EventType(str, Enum):
    presencial = "Presencial"
    virtual = "Virtual"


class Event(BaseModel):
    
    title: str = Field(default='Nuevo Evento', max_length=200)
    description: str = Field(default='sin Descripcion', max_length=200)
    start_time: datetime = Field(datetime(2024, 1, 4, 10, 0))
    finish_time: datetime = Field(datetime(2024, 1, 4, 11, 0))
    category: str = Field(default='Sin Categoria', max_length=50)    
    type: EventType = Field(default=EventType.presencial)
    location: str = Field(default='Sin Locacion')
    creator_id: int 
    

    def model_dump(self):
        return {
            
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "finish_time": self.finish_time,
            "category": self.category,            
            'type': self.type,
            'location': self.location,
            'creator_id': self.creator_id, 
            

        }

    class Config:
        schema_extra = {
            'example': {                
                'title': 'Nuevo Evento',
                'description': 'Sin descripcion',
                'start_time': datetime(2024, 1, 4, 10, 0),
                'finish_time': datetime(2024, 1, 4, 11, 0),
                'category': 'students',                
                'type': EventType.presencial,
                'location': 'Sin Locacion',               

            }
        }
        
class EventResponse(Event):
    id: int

    class Config:
        orm_mode = True
