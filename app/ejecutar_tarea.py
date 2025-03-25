import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from datetime import date
from app.models.exercise_logs import ExerciseLog
from app.models.user import User



def create_logs_for_all_users():
    db: Session = SessionLocal()

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
            # Crear el log con `completed: false`
            new_log = ExerciseLog(user_id=user.id, date=today, completed=False)
            db.add(new_log)
    
    db.commit()
    db.close()

# Configurar y registrar la tarea programada
scheduler = BackgroundScheduler()
scheduler.add_job(create_logs_for_all_users, "cron", hour=14, minute=8)  # Se ejecuta al final del día
scheduler.start()
