import logging
from datetime import date, datetime
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.exercise_logs import ExerciseLog
from app.models.user import User

# Configura la zona horaria de Colombia
colombia_tz = timezone("America/Bogota")

# Configurar logs para depuración
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("apscheduler").setLevel(logging.DEBUG)

# Función para crear logs de ejercicios para todos los usuarios
def create_logs_for_all_users():
    db: Session = SessionLocal()

    try:
        # Obtén todos los usuarios de la base de datos
        users = db.query(User).all()
        today = date.today()

        for user in users:
            # Verifica si ya existe un log para hoy
            log = (
                db.query(ExerciseLog)
                .filter(ExerciseLog.user_id == user.id, ExerciseLog.date == today)
                .first()
            )
            if not log:
                # Crear el log con `completed: False`
                new_log = ExerciseLog(user_id=user.id, date=today, completed=False)
                db.add(new_log)

        db.commit()
        logging.info(f"Logs created successfully for {len(users)} users on {today}")
    except Exception as e:
        logging.error(f"Error creating logs: {e}")
    finally:
        db.close()

# Configurar y registrar la tarea programada
scheduler = BackgroundScheduler()

# Registrar la tarea con la zona horaria de Colombia
scheduler.add_job(
    create_logs_for_all_users, 
    "cron", 
    hour=1, 
    minute=18, 
    timezone=colombia_tz
)

# Iniciar el programador
scheduler.start()
logging.info("Scheduler started")

# Mantener el script activo
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    logging.info("Scheduler stopped")
