from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de conexión a la base de datos desde la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar que la variable de entorno DATABASE_URL esté definida
if not DATABASE_URL:
    raise ValueError("Falta la variable de entorno DATABASE_URL en el archivo .env.")

# Crear el motor de la base de datos con la URL proporcionada
engine = create_engine(DATABASE_URL)

# Crear la sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base declarativa para definir los modelos
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
