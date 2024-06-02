from pydantic_settings import BaseSettings
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_host: str
    database_user: str
    database_password: str
    database_name: str
    database_url: str = None

    MAIL_USERNAME: str = "eventmaster24@outlook.com"
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr = "eventmaster24@outlook.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.office365.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM_NAME: str = "Event Master"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database_url = (
            f"postgresql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}/{self.database_name}"
        )

    class Config:
        env_file = ".env"
        fields = {
            'database_host': 'DATABASE_HOST',
            'database_user': 'DATABASE_USER',
            'database_password': 'DATABASE_PASSWORD',
            'database_name': 'DATABASE_NAME',
            'mail_password': 'MAIL_PASSWORD'
        }

settings = Settings()