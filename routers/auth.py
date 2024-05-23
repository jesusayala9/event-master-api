from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.token import Token
from schemas.user_created import UserCreate
from services.auth import create_access_token, get_password_hash, authenticate_user, get_current_active_user, get_db
from schemas.auth import User_Auth
from schemas.user import Users 
from models.user import Users as UsersModel  

auth_router = APIRouter()

class AuthController:
    @auth_router.post("/register", tags=['Auth'], response_model=Users)
    def register_user(user: UserCreate, db: Session = Depends(get_db)):
        db_user = db.query(UsersModel).filter(UsersModel.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = get_password_hash(user.password)
        db_user = UsersModel(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(content={"message": "User registered successfully"})

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