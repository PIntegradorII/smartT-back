from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

class Settings(BaseSettings):
    # Configuración de la base de datos
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Configuración del servidor
    SERVER_HOST: str
    SERVER_PORT: int

    # Configuración de autenticación
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Variables opcionales
    DEBUG: bool = False  # Valor por defecto False si no está en el .env

    class Config:
        env_file = ".env"
        extra = "allow"  # Permite variables adicionales en .env

# Instancia global de configuración
settings = Settings()
