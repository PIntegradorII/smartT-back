from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.training_plan import TrainingPlan
from app.models.user import User
from app.schemas.training_plan import TrainingPlanCreate  
from app.services.training_service import generar_plan_entrenamiento
import json  # Importar para convertir JSON a String

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
    """Genera un plan de entrenamiento basado en los datos del usuario (NO lo guarda)"""
    
    condiciones_list = condiciones_medicas.split(",")  # Convertir condiciones a lista

    plan = generar_plan_entrenamiento({
        "nombre": nombre,
        "peso": peso,
        "altura": altura,
        "sexo": sexo,
        "condiciones_medicas": condiciones_list,
        "meta_entrenamiento": meta_entrenamiento
    })

    if not plan:
        raise HTTPException(status_code=400, detail="No se pudo generar el plan de entrenamiento")
    
    return plan


@router.post("/training-plan")
def create_training_plan(plan_data: TrainingPlanCreate, db: Session = Depends(get_db)):
    """ Guarda un plan de entrenamiento en la base de datos """

    # Convertir los datos a strings JSON
    new_plan = TrainingPlan(
        user_id=plan_data.user_id,
        plan={
            "lunes": json.dumps(plan_data.lunes or {}),
            "martes": json.dumps(plan_data.martes or {}),
            "miercoles": json.dumps(plan_data.miercoles or {}),
            "jueves": json.dumps(plan_data.jueves or {}),
            "viernes": json.dumps(plan_data.viernes or {}),
        }
    )

    # Guardar en la base de datos
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return {"message": "Plan de entrenamiento guardado", "plan_id": new_plan.id}


def double_json_loads(value):
    """Aplica json.loads() dos veces si es necesario"""
    try:
        if isinstance(value, str):  # Si es string, intenta decodificarlo
            value = json.loads(value)
        if isinstance(value, str):  # A veces los datos están doblemente serializados
            value = json.loads(value)
        return value
    except json.JSONDecodeError:
        return None  # Evita errores si la conversión falla

@router.get("/training-plan/google/{google_id}")
def get_training_plan_by_google_id(google_id: str, db: Session = Depends(get_db)):
    """Obtiene el plan de entrenamiento de un usuario usando su google_id"""
    
    # 1. Buscar el usuario por google_id
    user = db.query(User).filter(User.google_id == google_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Obtener el ID del usuario
    user_id = user.id

    # 3. Buscar el plan de entrenamiento asociado al usuario
    plan = db.query(TrainingPlan).filter(TrainingPlan.user_id == user_id).first()
    print(plan)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de entrenamiento no encontrado")

    # 4. Convertir los campos JSON doblemente serializados
    json_fields = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    for field in json_fields:
        setattr(plan, field, double_json_loads(getattr(plan, field)))

    return plan




