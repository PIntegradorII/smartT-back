from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from app.core.config import settings

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de conexión a la base de datos desde settings o desde el .env
DATABASE_URL = settings.DATABASE_URL if hasattr(settings, "DATABASE_URL") else os.getenv("DATABASE_URL")

# Validar que DATABASE_URL no sea None o una cadena vacía
if not DATABASE_URL:
    raise ValueError("❌ Falta la variable de entorno DATABASE_URL en el archivo .env.")

# Crear el motor de base de datos con parámetros adicionales
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    echo=False  # Cambiar a True para depuración
)

# Crear sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir modelos SQLAlchemy
Base = declarative_base()

# Función para probar la conexión a la base de datos
def test_db_connection():
    try:
        with engine.connect() as connection:
            print("✅ Conexión a la base de datos establecida correctamentes.")
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")

# Llamar a la función de prueba al iniciar la aplicación
test_db_connection()

# Dependencia para obtener una sesión de base de datos
def get_db() -> Session:
    """Crea y cierra una sesión de base de datos de manera segura."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"❌ Error en la sesión de base de datos: {e}")
        db.rollback()  # Revertir cambios en caso de error
        raise
    finally:
        db.close()
