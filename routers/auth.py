from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.token import Token
from schemas.user_created import UserCreate
from services.auth import create_access_token, get_password_hash, authenticate_user, get_current_active_user, get_db
from schemas.auth import User_Auth
from schemas.user import Users 
from models.user import Users as UsersModel
from config.config_mail import settings


auth_router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='templates'
)


class AuthController:
    
    @auth_router.post("/register", tags=['Auth'], response_model=Users)
    async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
        try:
            # Check if username is already registered
            db_user = db.query(UsersModel).filter(UsersModel.username == user.username).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Username already registered")

            # Check if email is already registered
            db_user = db.query(UsersModel).filter(UsersModel.email == user.email).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")

            # Hash the password and create new user record
            hashed_password = get_password_hash(user.password)
            db_user = UsersModel(username=user.username, email=user.email, hashed_password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
            # Send confirmation email
            message = MessageSchema(
                subject="Welcome to Event Master",
                recipients=[user.email],
                body=f"Hello {user.username}, welcome to Event Master!",
                subtype="html"
            )

            try:
                fm = FastMail(conf)
                background_tasks.add_task(fm.send_message, message)
                print(f"Confirmation email sent to: {user.email}")
            except Exception as e:
                print(f"Failed to send confirmation email to: {user.email}. Error: {e}")

            return JSONResponse(content={"message": "User registered successfully"})

        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during registration: {e}")
    
    
    

    @auth_router.post("/token", tags=['Auth'], response_model=Token)
    def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @auth_router.get('/me', tags=['Auth'], response_model=Users)
    def get_current_user(current_user: Users = Depends(get_current_active_user)):
        return current_user