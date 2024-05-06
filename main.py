from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
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


