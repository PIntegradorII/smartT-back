import os

# Ruta base del proyecto
base_path = r"B:\Universidad\IntegradorII\PIntegrador-back"

directories = [
    "app/api/v1",
    "app/core",
    "app/models",
    "app/schemas",
    "app/services",
    "app/db",
    "tests"
]

files = {
    "app/api/v1/auth.py": """# Endpoints para autenticación
from fastapi import APIRouter
router = APIRouter()

@router.post('/login')
def login():
    return {"message": "Login exitoso"}
""",
    "app/api/v1/users.py": """# Endpoints para usuarios
from fastapi import APIRouter
router = APIRouter()

@router.get('/users')
def get_users():
    return {"users": []}
""",
    "app/api/v1/routines.py": """# Endpoints de rutinas fitness
from fastapi import APIRouter
router = APIRouter()

@router.get('/routines')
def get_routines():
    return {"routines": []}
""",
    "app/api/v1/health.py": """# Endpoints de historial médico
from fastapi import APIRouter
router = APIRouter()

@router.get('/health')
def get_health():
    return {"health": []}
""",
    "app/api/v1/exercises.py": """# Endpoints de ejercicios
from fastapi import APIRouter
router = APIRouter()

@router.get('/exercises')
def get_exercises():
    return {"exercises": []}
""",
    "app/core/config.py": """# Variables de entorno y configuración general
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

settings = Settings()
""",
    "app/core/security.py": """# Configuración de JWT y OAuth
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
""",
    "app/models/user.py": """# Modelo de usuario
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
""",
    "app/db/database.py": """# Configuración de la base de datos
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
""",
    "app/main.py": """# Punto de entrada de la aplicación
from fastapi import FastAPI
from app.api.v1 import auth, users, routines, health, exercises

app = FastAPI()

app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(routines.router, prefix="/v1/routines", tags=["Routines"])
app.include_router(health.router, prefix="/v1/health", tags=["Health"])
app.include_router(exercises.router, prefix="/v1/exercises", tags=["Exercises"])
"""
}

# Crear directorios
for directory in directories:
    full_path = os.path.join(base_path, directory)
    os.makedirs(full_path, exist_ok=True)

# Crear archivos con contenido
for file, content in files.items():
    file_path = os.path.join(base_path, file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)