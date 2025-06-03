from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware# Importar el nuevo módulo
from app.api.v1 import auth, users, routines, health, ingredients, exercises,diet, personal_data, training, log_exercises, physical, training_plan_history, physical_history, hist_recetas,  img_maquinas, img_platos, barcode # Importar el nuevo módulo
from app.core.config import settings
from app.db.database import test_db_connection
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import logging
import locale
from app.ejecutar_tarea import create_logs_for_all_users
from app.services.watson import speech_to_text
import os
# ✅ Instancia de FastAPI
app = FastAPI(debug=settings.DEBUG)


# Inicializa los servicios una ve




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

current_time = datetime.now().strftime("%A, %d de %B de %Y %H:%M:%S")
print(f"🕒 Hora actual: {current_time}")


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
app.include_router(diet.router, prefix="/v1/diet", tags=["Diet"])
app.include_router(training_plan_history.router, prefix="/v1/training_plan_history", tags=["Training_plan_history"])
app.include_router(ingredients.router, prefix="/v1/ingredientes", tags=["Ingredients"])
app.include_router(physical_history.router, prefix="/v1/physical_history", tags=["Measures"])

app.include_router(hist_recetas.router, prefix="/v1/hist_recetas", tags=["hist_recetas"])
app.include_router(img_maquinas.router, prefix="/v1/img_maquinas", tags=["img_maquinas"])
app.include_router(img_platos.router, prefix="/v1/img_platos", tags=["img_platos"])
app.include_router(barcode.router, prefix="/v1/barcode", tags=["img_barcode"])