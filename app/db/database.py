from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Construcción de la URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = (
    f"mysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para verificar la conexión a la base de datos
def test_db_connection():
    try:
        with engine.connect() as connection:
            print("✅ Conexión a la base de datos establecida correctamente.")
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")

# Llamar a la función de prueba de conexión al iniciar la aplicación
test_db_connection()

# Dependencia para obtener una sesión de base de datos
def get_db() -> Session:
    """Dependencia para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
