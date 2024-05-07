from pydantic import BaseModel, Field

class Users(BaseModel):
    id: int
    username: str = Field(default='jhon', max_length=20)
    email: str = Field(default='jhon@mail.com', max_length=20)
    password: str = Field(default='12345@', max_length=20)
    events: list = Field(default=['Evento1', 'Evento2'])
    created_events: list = Field(default=['Evento3', 'Evento4'])
 

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