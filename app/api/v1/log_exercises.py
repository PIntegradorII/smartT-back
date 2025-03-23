from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.exercise_logs import (
    create_exercise_log,
    get_exercise_logs_by_google_id,
    update_exercise_log,
    delete_exercise_log,
)
from app.schemas.exercise_logs import ExerciseLogCreate, ExerciseLogRequest, ExerciseLogUpdate, ExerciseLogResponse,ExerciseLogResponseLog
from datetime import date
from app.models.exercise_logs import ExerciseLog, User
from pydantic import BaseModel

class GoogleIDRequest(BaseModel):
    google_id: str


router = APIRouter()

# ✅ Crear un registro de ejercicio
@router.post("/exercise/", response_model=ExerciseLogResponse)
def mark_exercise(log_data: ExerciseLogCreate, db: Session = Depends(get_db)):
    try:
        return create_exercise_log(db, log_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
    
@router.get("/exercise/{log_id}", response_model=ExerciseLogResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ExerciseLog).filter(ExerciseLog.user_id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return log


@router.post("/exercise/weekly/", response_model=List[dict])
def get_exercise_logs(request: ExerciseLogRequest, db: Session = Depends(get_db)):
    logs = get_exercise_logs_by_google_id(db, request.google_id)
    
    if not logs:
        raise HTTPException(status_code=404, detail="No se encontraron registros para este usuario")
    
    # Mapeo de los registros a la estructura deseada
    weekday_map = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
        4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    
    weekly_summary = []
    for log in logs:
        date_obj = log.date  # Asegurar que es un objeto datetime.date
        day_name = weekday_map[date_obj.weekday()]  # Obtener nombre del día en español
        formatted_date = date_obj.strftime("%d de %B")  # Formato "22 de marzo"
        
        weekly_summary.append({
            "day": day_name,
            "completed": log.completed,
            "date": formatted_date
        })
    
    return weekly_summary