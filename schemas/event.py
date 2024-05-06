from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class EventType(str, Enum):
    presencial = "Presencial"
    virtual = "Virtual"

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