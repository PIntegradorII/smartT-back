from fastapi import APIRouter
from app.services.training_service import generar_plan_entrenamiento
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.training_service import generar_plan_entrenamiento
from app.db.database import get_db
from app.models.user import User  # Asegúrate de tener el modelo del usuario definido
router = APIRouter()

@router.get("/training-plan")
def get_training_plan():
    """Endpoint para obtener el plan de entrenamiento"""
    plan = generar_plan_entrenamiento()
    if not plan:
        return {"error": "No se pudo generar el plan de entrenamiento"}
    return plan

@router.get("/user_data")
def get_user_data(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Consulta todos los usuarios
    return users  # FastAPI serializa automáticamente los datos