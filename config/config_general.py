from pydantic_settings import BaseSettings
from pydantic import  EmailStr,  BaseModel, validator
from dotenv import load_dotenv
import os

load_dotenv()


class ConfigGeneral(BaseModel):
    database_user: str
    database_password: str
    database_name: str
    database_host: str
    database_url: str = None

    MAIL_USERNAME: str = "eventmaster24@outlook.com"
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr = "eventmaster24@outlook.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.office365.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM_NAME: str = "Event Master"

    @validator("database_url", pre=True, always=True)
    def assemble_db_connection(cls, v, values):
        if all(values.get(f) for f in ['database_user', 'database_password', 'database_host', 'database_name']):
            return f"postgresql://{values['database_user']}:{values['database_password']}@{values['database_host']}/{values['database_name']}"
        return v

settings = ConfigGeneral(
    database_user=os.getenv("DATABASE_USER"),
    database_password=os.getenv("DATABASE_PASSWORD"),
    database_name=os.getenv("DATABASE_NAME"),
    database_host=os.getenv("DATABASE_HOST"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
)