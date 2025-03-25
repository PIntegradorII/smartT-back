from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, routines, health, exercises, personal_data, training, log_exercises, physical  # Importar el nuevo módulo
from app.core.config import settings
from app.db.database import test_db_connection
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime
import logging
import locale
from app.ejecutar_tarea import create_logs_for_all_users
# ✅ Instancia de FastAPI
app = FastAPI(debug=settings.DEBUG)

# ✅ Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Configurar logging para eventos del scheduler
logging.basicConfig(level=logging.INFO)

# # ✅ Configurar Locale
try:
     locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
     print("⚠️ No se pudo establecer el locale 'es_ES.UTF-8'. Usando el predeterminado.")

print(f"🌍 Locale actual: {locale.getlocale()}")



# ✅ Agregar eventos para el seguimiento del scheduler
def job_listener(event):
    if event.exception:
        logging.error(f"❌ Error en la tarea programada: {event.job_id}")
    else:
        logging.info(f"✅ Tarea ejecutada correctamente: {event.job_id}")

# ✅ Iniciar el programador de tareas
scheduler = BackgroundScheduler()
#scheduler.add_job(create_logs_for_all_users, "cron", hour=13, minute=47, max_instances=1)  # Ejecutar a las 00:00 cada día
#scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

# ✅ Eventos de inicio y cierre
@app.on_event("startup")
def startup_event():
    test_db_connection()  # Verificar conexión a la BD
    if not scheduler.running:
        print("🔄 Iniciando APScheduler...")
        scheduler.start()  # Inicia el programador solo si no está corriendo

@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Deteniendo APScheduler...")
    scheduler.shutdown()



# ✅ Endpoint de prueba
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

# ✅ Registrar los routers
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(routines.router, prefix="/v1/routines", tags=["Routines"])
app.include_router(health.router, prefix="/v1/health", tags=["Health"])
app.include_router(exercises.router, prefix="/v1/exercises", tags=["Exercises"])
app.include_router(personal_data.router, prefix="/v1/personal_data", tags=["PersonalData"])
app.include_router(training.router, prefix="/v1/training", tags=["Training"])
app.include_router(log_exercises.router, prefix="/v1/log_exercises", tags=["LogExercises"])
app.include_router(physical.router, prefix="/v1/physical", tags=["Physical"]) 