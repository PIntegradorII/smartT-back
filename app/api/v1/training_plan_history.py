from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.db.database import get_db
from app.schemas.training_plan_history import TrainingPlanHistorySchema
from app.services.training_plan_history import get_training_plan_history

router = APIRouter()

@router.get("/history/{google_id}", response_model=List[TrainingPlanHistorySchema])
def get_routine_history(google_id: str, db: Session = Depends(get_db)):
    """
    Obtiene el historial de rutinas de un usuario basado en su Google ID.
    """
    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return get_training_plan_history(db, user.id)  # Se usa el ID real del usuario
