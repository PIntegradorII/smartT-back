from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.exercise_logs import (
    create_exercise_log,
    update_exercise_log,
    get_weekly_summary,
    delete_exercise_log,
)
from app.schemas.exercise_logs import ExerciseLogCreate, ExerciseLogUpdate, ExerciseLogResponse
from datetime import date
from app.models.exercise_logs import ExerciseLog, User





router = APIRouter()

# ✅ Crear un registro de ejercicio
@router.post("/exercise/", response_model=ExerciseLogResponse)
def mark_exercise(log_data: ExerciseLogCreate, db: Session = Depends(get_db)):
    try:
        return create_exercise_log(db, log_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Obtener el resumen semanal
@router.get("/exercise/summary/")
def get_summary(user_id: int, db: Session = Depends(get_db)):
    return get_weekly_summary(db, user_id)

# ✅ Actualizar un registro de ejercicio
@router.patch("/exercise/{log_id}", response_model=ExerciseLogResponse)
def update_log(log_id: int, log_data: ExerciseLogUpdate, db: Session = Depends(get_db)):
    try:
        return update_exercise_log(db, log_id, log_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ✅ Eliminar un registro de ejercicio
@router.delete("/exercise/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    if not delete_exercise_log(db, log_id):
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro eliminado"}


@router.post("/check_exercises")
def check_unlogged_exercises(db: Session = Depends(get_db)):
    try:
        today = date.today()
        users = db.query(User).all()

        for user in users:
            exercise_exists = db.query(ExerciseLog).filter(
                ExerciseLog.user_id == user.id,
                ExerciseLog.date == today
            ).first()

            if not exercise_exists:
                new_log = ExerciseLog(user_id=user.id, date=today, completed=False)
                db.add(new_log)

        db.commit()
        return {"message": "Tarea ejecutada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar ejercicios: {str(e)}")
