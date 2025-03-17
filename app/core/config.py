from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from urllib.parse import urlparse

# Cargar las variables desde el archivo .env
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVER_HOST: str
    SERVER_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool = False

    FIREBASE_API_KEY: str
    FIREBASE_AUTH_DOMAIN: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_STORAGE_BUCKET: str
    FIREBASE_MESSAGING_SENDER_ID: str
    FIREBASE_APP_ID: str
    FIREBASE_MEASUREMENT_ID: str

    class Config:
        env_file = ".env"
        extra = "allow"  # Permite variables adicionales en .env

    @property
    def db_host(self):
        return urlparse(self.DATABASE_URL).hostname

    @property
    def db_port(self):
        return urlparse(self.DATABASE_URL).port

    @property
    def db_name(self):
        return urlparse(self.DATABASE_URL).path.lstrip("/")

    @property
    def db_user(self):
        return urlparse(self.DATABASE_URL).username

    @property
    def db_password(self):
        return urlparse(self.DATABASE_URL).password

settings = Settings()
