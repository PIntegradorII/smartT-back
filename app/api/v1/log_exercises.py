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

@router.get("/exercise/completed/")
def is_exercise_completed(user_id: int, exercise_date: date = date.today(), db: Session = Depends(get_db)):
    log = (
        db.query(ExerciseLog)
        .filter(ExerciseLog.user_id == user_id, ExerciseLog.date == exercise_date)
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="No se encontró registro para esta fecha.")
    return {"user_id": user_id, "date": exercise_date, "completed": log.completed}

@router.get("/exercise/logs")
def get_log_by_user_and_date(user_id: int, date: date, db: Session = Depends(get_db)):
    log = (
        db.query(ExerciseLog)
        .filter(ExerciseLog.user_id == user_id, ExerciseLog.date == date)
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="Log no encontrado para esta fecha.")
    return {"user_id": log.user_id, "date": log.date, "completed": log.completed}


@router.patch("/exercise/logs/")
def update_log_by_user_and_date(
    user_id: int,
    date: date,
    completed: int,
    db: Session = Depends(get_db),
):
    log = (
        db.query(ExerciseLog)
        .filter(ExerciseLog.user_id == user_id, ExerciseLog.date == date)
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="Log no encontrado para esta fecha.")
    
    # Actualizar el campo "completed"
    log.completed = completed
    db.commit()
    db.refresh(log)
    
    return {"user_id": log.user_id, "date": log.date, "completed": log.completed}
    


@router.get("/exercise/{google_id}", response_model=ExerciseLogResponse)
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
    
    weekday_map = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
        4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    
    weekly_summary = []
    for log in logs:
        date_obj = log.date  # Asegurar que es un objeto datetime.date
        day_name = weekday_map[date_obj.weekday()]
        formatted_date = date_obj.strftime("%d de %B")
        
        weekly_summary.append({
            "day": day_name,
            "completed": log.completed,
            "date": formatted_date,
            "date_obj": date_obj  # Agregar el objeto fecha para ordenación
        })

    # Ordenar por fecha en orden ascendente
    weekly_summary = sorted(weekly_summary, key=lambda x: x["date_obj"])

    # Remover el campo auxiliar 'date_obj' antes de retornar
    for entry in weekly_summary:
        del entry["date_obj"]

    return weekly_summary
