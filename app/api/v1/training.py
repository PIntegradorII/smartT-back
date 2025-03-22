from fastapi import APIRouter
from app.services.training_service import generar_plan_entrenamiento

router = APIRouter()

@router.get("/training-plan", tags=["Training"])
def get_training_plan():
    """Endpoint para obtener el plan de entrenamiento"""
    plan = generar_plan_entrenamiento()
    if not plan:
        return {"error": "No se pudo generar el plan de entrenamiento"}
    return plan
