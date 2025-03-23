from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
from app.models.exercise_logs import ExerciseLog
from app.schemas.exercise_logs import ExerciseLogCreate, ExerciseLogUpdate, ExerciseLogResponse
from app.models.user import User
# ✅ Registrar un nuevo log de ejercicio
def create_exercise_log(db: Session, log_data: ExerciseLogCreate) -> ExerciseLogResponse:
    try:
        # Validar existencia del usuario
        user_exists = db.query(User).filter(User.id == log_data.user_id).first()
        if not user_exists:
            raise ValueError(f"Usuario con id {log_data.user_id} no existe.")

        # Crear registro
        db_log = ExerciseLog(**log_data.model_dump())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error de integridad: {str(e.orig)}")


# ✅ Actualizar un log de ejercicio
def update_exercise_log(db: Session, log_id: int, log_data: ExerciseLogUpdate) -> ExerciseLogResponse:
    db_log = db.get(ExerciseLog, log_id)
    if not db_log:
        raise ValueError("Registro no encontrado")

    for key, value in log_data.model_dump(exclude_unset=True).items():
        setattr(db_log, key, value)

    db.commit()
    db.refresh(db_log)
    return db_log

# ✅ Obtener el resumen semanal del usuario
def get_weekly_summary(db: Session, user_id: int):
    today = date.today()
    start_week = today - timedelta(days=today.weekday())  # Lunes de la semana actual

    logs = (
        db.query(ExerciseLog)
        .filter(ExerciseLog.user_id == user_id, ExerciseLog.date >= start_week)
        .order_by(ExerciseLog.date)
        .all()
    )

    summary = {
        "user_id": user_id,
        "week_start": start_week,
        "week_end": start_week + timedelta(days=6),
        "logs": [{"date": log.date, "completed": log.completed} for log in logs],
    }

    return summary

# ✅ Eliminar un registro de ejercicio
def delete_exercise_log(db: Session, log_id: int) -> bool:
    db_log = db.get(ExerciseLog, log_id)
    if not db_log:
        return False
    db.delete(db_log)
    db.commit()
    return True
