from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta, datetime
from app.models.user import User
from app.schemas.exercise_logs import ExerciseLogCreate, ExerciseLogUpdate, ExerciseLogResponse
from app.models.exercise_logs import ExerciseLog

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


# ✅ Eliminar un registro de ejercicio
def delete_exercise_log(db: Session, log_id: int) -> bool:
    db_log = db.get(ExerciseLog, log_id)
    if not db_log:
        return False
    db.delete(db_log)
    db.commit()
    return True

def get_exercise_logs_by_google_id(db: Session, google_id: str):
    """
    Obtiene los registros de ejercicio del usuario con el google_id proporcionado solo para la semana actual (lunes a domingo).
    """
    user = db.query(User).filter(User.google_id == google_id).first()
    print(user.id)
    if not user:
        return None  # Usuario no encontrado
    
    # Obtener la fecha actual
    today = datetime.today().date()  # Convertimos a `date` para evitar problemas con `datetime`
    
    # Determinar el lunes de la semana actual
    start_of_week = today - timedelta(days=today.weekday())  # Lunes de la semana actual
    end_of_week = start_of_week + timedelta(days=6)  # Domingo de la semana actual
    
    return db.query(ExerciseLog).filter(
        ExerciseLog.user_id == user.id,
        ExerciseLog.date >= start_of_week,
        ExerciseLog.date <= end_of_week
    ).all()