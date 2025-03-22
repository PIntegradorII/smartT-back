from fastapi import APIRouter, Query
from app.services.training_service import generar_plan_entrenamiento
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User  # Asegúrate de tener el modelo del usuario definido
router = APIRouter()

@router.get("/training-plan")
def get_training_plan(
    nombre: str = Query(..., description="Nombre del usuario"),
    peso: float = Query(..., description="Peso en kg"),
    altura: float = Query(..., description="Altura en metros"),
    sexo: str = Query(..., description="Sexo del usuario"),
    condiciones_medicas: str = Query("Ninguna", description="Condiciones médicas"),
    meta_entrenamiento: str = Query(..., description="Meta de entrenamiento"),
):
    """Endpoint para obtener el plan de entrenamiento basado en los datos del usuario"""
    
    # Convertir condiciones médicas en lista si hay más de una
    condiciones_list = condiciones_medicas.split(",")

    # Generar plan de entrenamiento
    plan = generar_plan_entrenamiento({
        "nombre": nombre,
        "peso": peso,
        "altura": altura,
        "sexo": sexo,
        "condiciones_medicas": condiciones_list,
        "meta_entrenamiento": meta_entrenamiento
    })

    if not plan:
        return {"error": "No se pudo generar el plan de entrenamiento"}
    
    return plan