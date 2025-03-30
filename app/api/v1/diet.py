from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import requests
import os
from app.services.watson import speech_to_text
import logging
from app.models.diet import DietPlan
from app.schemas.diet import DietPlanCreate, DietPlanResponse
from sqlalchemy.orm import Session
from app.db.database import get_db


# Cargar las claves y URLs desde las variables de entorno
STT_API_KEY = os.getenv("IBM_STT_API_KEY")
STT_URL = os.getenv("IBM_STT_URL")

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/voice-to-text")
async def voice_to_text(audio: UploadFile = File(...)):
    try:
        logger.info(f"Nombre del archivo recibido: {audio.filename}")
        logger.info(f"Tipo de contenido: {audio.content_type}")
        audio_bytes = await audio.read()
        logger.info(f"Tamaño del archivo: {len(audio_bytes)} bytes")

        # Verificar si el tipo de archivo es correcto
        if audio.content_type != "audio/wave":
            raise HTTPException(status_code=400, detail="El archivo debe ser de tipo audio/wav.")
        
        # Llamar a Watson Speech to Text
        transcript = speech_to_text(audio_bytes, content_type="audio/wav")
        logger.info(f"Transcripción recibida: {transcript}")
        
        return {"transcript": transcript}
    except Exception as e:
        logger.error(f"Error procesando el archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento: {str(e)}")

# Crear un nuevo diet plan
@router.post("/diet-plan/", response_model=DietPlanResponse)
async def create_diet_plan(diet_plan: DietPlanCreate, db: Session = Depends(get_db)):
    try:
        # Crear un nuevo registro de diet plan
        db_diet_plan = DietPlan(**diet_plan.dict())
        db.add(db_diet_plan)
        db.commit()
        db.refresh(db_diet_plan)  # Recargar el objeto después de insertarlo para obtener el id generado
        return db_diet_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando el plan de dieta: {str(e)}")

# Obtener todos los diet plans para un usuario
@router.get("/diet-plan/{user_id}", response_model=list[DietPlanResponse])
async def get_diet_plans(user_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener los planes de dieta del usuario
        diet_plans = db.query(DietPlan).filter(DietPlan.user_id == user_id).all()
        if not diet_plans:
            raise HTTPException(status_code=404, detail="Planes de dieta no encontrados para este usuario.")
        return diet_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo los planes de dieta: {str(e)}")

# Obtener un plan de dieta por su id
@router.get("/diet-plan/{diet_plan_id}", response_model=DietPlanResponse)
async def get_diet_plan(diet_plan_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener un plan de dieta por su ID
        diet_plan = db.query(DietPlan).filter(DietPlan.id == diet_plan_id).first()
        if not diet_plan:
            raise HTTPException(status_code=404, detail="Plan de dieta no encontrado.")
        return diet_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo el plan de dieta: {str(e)}")