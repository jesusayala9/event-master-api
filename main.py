from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, SessionLocal, Base
from middlewares.error_handler import ErrorHandler
from routers.event import event_router
from routers.auth import auth_router
from routers.user import user_router


app = FastAPI()
app.title = 'EventMaster API'
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(event_router)
app.include_router(auth_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')


# class User(BaseModel):
#     email: str
#     password: str


# datetime(año, mes, dia, hora, min, segundo)

# Se validan los datos con la propiedad Field

    # id: int
    # title: str = Field(default='Nuevo Evento', max_length=20)
    # description: str = Field(default='sin Descripcion', max_length=50)
    # startTime: datetime = Field(datetime(2024, 1, 4, 10, 0))
    # finishTime: datetime = Field(datetime(2024, 1, 4, 11, 0))
    # category: str = Field(default='Sin Categoria', max_length=20)
    # audience: int = Field(default=0)
    # type: EventType = Field(default=EventType.presencial)
    # location: str = Field(default='Sin Locacion')

    # def model_dump(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "description": self.description,
    #         "startTime": self.startTime,
    #         "finishTime": self.finishTime,
    #         "category": self.category,
    #         "audience": self.audience,
    #         'type': self.type,
    #         'location': self.location
    #     }

    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'id': 1,
    #             'title': 'Nuevo Evento',
    #             'description': 'Sin descripcion',
    #             'startTime': datetime(2024, 1, 4, 10, 0),
    #             'finishTime': datetime(2024, 1, 4, 11, 0),
    #             'category': 'students',
    #             'audience': 0,
    #             'type': EventType.presencial,
    #             'location': 'Sin Locacion'
    #         }
    #     }


# events = [
#     {
#         'id': 1,
#         'title': 'DevFest',
#         'description': 'asdasd',
#         'startTime': datetime(2024, 1, 4, 10, 0),
#         'finishTime': datetime(2024, 1, 4, 11, 0),
#         'category': 'tedtalk',
#         'audience': 10,
#         'type': EventType.presencial,
#         'location': 'Tulua'
#     },

#     {
#         'id': 2,
#         'title': 'JsConf',
#         'description': 'asdasd',
#         'startTime': datetime(2024, 1, 4, 10, 0),
#         'finishTime': datetime(2024, 1, 4, 11, 0),
#         'category': 'students',
#         'audience': 20,
#         'type': EventType.presencial,
#         'location': 'Tulua'
#     },
# ]


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# db_dependency = Annotated[Session, Depends(get_db)]





# @app.post('/login', tags=['auth'])
# def login(user: User):
#     if user.email == "admin@gmail.com" and user.password == "admin":
#         token: str = create_token(user.model_dump())
#         return JSONResponse(status_code=200, content=token)
