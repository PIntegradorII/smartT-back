from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, routines, health, exercises, personal_data
from app.core.config import settings
from app.db.database import test_db_connection

app = FastAPI(debug=settings.DEBUG)

test_db_connection()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Combina los orígenes aquí
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los encabezados
)

# Endpoint raíz para evitar el error 404
@app.get("/")
def root():
    return {"message": "API funcionando correctamente. Consulta /docs para más información."}

@app.get("/config")
def get_config():
    return {
        "database_url": f"{settings.DB_USER}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
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