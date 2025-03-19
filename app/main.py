# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, routines, health, exercises, personal_data
from app.core.config import settings
from app.db.database import test_db_connection


# Crear la instancia de FastAPI
app = FastAPI(debug=settings.DEBUG)

# Verificación de conexión a la base de datos
test_db_connection()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente. Consulta /docs para más información."}

@app.get("/config")
def get_config():
    return {
        "database_url": settings.DATABASE_URL,
        "server_host": settings.SERVER_HOST,
        "server_port": settings.SERVER_PORT,
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
        "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "debug": settings.DEBUG
    }

# Registrar los routers
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(routines.router, prefix="/v1/routines", tags=["Routines"])
app.include_router(health.router, prefix="/v1/health", tags=["Health"])
app.include_router(exercises.router, prefix="/v1/exercises", tags=["Exercises"])
app.include_router(personal_data.router, prefix="/v1/personal_data", tags=["PersonalData"])