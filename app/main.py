from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, routines, health, exercises, personal_data, training, log_exercises
from app.core.config import settings
from app.db.database import test_db_connection
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime
import logging
from fastapi import FastAPI
from app.ejecutar_tarea import scheduler  # Importa el programador
import locale
import os


# Crear la instancia de FastAPI
app = FastAPI(debug=settings.DEBUG)
# Eventos de inicio y cierre
@app.on_event("startup")
def startup_event():
    if not scheduler.running:
        scheduler.start()# Inicia el programador al iniciar la aplicación

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown() 
# Verificación de conexión a la base de datos
test_db_connection()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar logging para eventos del job scheduler
logging.basicConfig(level=logging.INFO)



# Configurar el Locale
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    print("⚠️ No se pudo establecer el locale 'es_ES.UTF-8'. Usando el predeterminado.")

# Obtener la configuración del locale actual
print(f"🌍 Locale actual: {locale.getlocale()}")




# ✅ Función que se ejecutará en segundo plano
def marcar_no_registrado():
    try:
        url = "http://127.0.0.1:8000/check_exercises"  # Cambia esto por la URL de tu API
        response = requests.post(url)
        response.raise_for_status()  # Lanzar una excepción si la respuesta es un error HTTP
        print(f"Respuesta de la API: {response.status_code} - {datetime.datetime.now()}")
    except requests.exceptions.RequestException as e:
        print(f"Error al ejecutar la tarea en segundo plano: {str(e)}")
        logging.error(f"Error al ejecutar la tarea en segundo plano: {str(e)}")

# Agregar eventos para el seguimiento de la tarea programada
def job_listener(event):
    if event.exception:
        logging.error(f"Error en la tarea programada: {event.job_id}")
    else:
        logging.info(f"Tarea ejecutada correctamente: {event.job_id}")

# Iniciar el programador de tareas
scheduler = BackgroundScheduler()
# Agregar la tarea para que se ejecute todos los días a medianoche
scheduler.add_job(marcar_no_registrado, "cron", hour=0, minute=0)  # Ejecutar a las 00:00 cada día
scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.start()

# ✅ Endpoint para ejecutar la tarea en segundo plano
@app.post("/run_background_task")
def run_background_task(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(marcar_no_registrado)
        return {"message": "Tarea en segundo plano iniciada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar la tarea: {str(e)}")

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
app.include_router(training.router, prefix="/v1/training", tags=["Training"])
app.include_router(log_exercises.router, prefix="/v1/log_exercises", tags=["LogExercises"])
