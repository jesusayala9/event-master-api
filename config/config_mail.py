from pydantic_settings import BaseSettings
from pydantic import  EmailStr


class Settings(BaseSettings):
    MAIL_USERNAME: str = "eventmaster24@outlook.com"
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr = "eventmaster24@outlook.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.office365.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM_NAME: str = "Event Master"

    class Config:
        env_file = ".env"

settings = Settings()