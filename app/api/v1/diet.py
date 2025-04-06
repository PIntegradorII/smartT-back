from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
import requests
import os
from app.services.watson import speech_to_text
import logging
from app.models.diet import DietPlan
from app.schemas.diet import DietPlanCreate, DietPlanResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.diet import get_diet_plan, save_or_update_recipe
from app.db.database import Session, get_db
from app.models.user import User
from app.services.watson import speech_to_text
import json


# Cargar las claves y URLs desde las variables de entorno
STT_API_KEY = os.getenv("IBM_STT_API_KEY")
STT_URL = os.getenv("IBM_STT_URL")

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/voice-to-text")
async def voice_to_text( google_id: str = Form(...),  # Usar Form para google_id
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)  # Usar File para el archivo de audio
):
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

        # Generar el plan alimenticio basado en la transcripción
        diet_plan = get_diet_plan(transcript)
        logger.info(f"Plan alimenticio generado: {diet_plan}")

        user = db.query(User).filter(User.google_id == google_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")


        save_or_update_recipe(user.id, transcript, diet_plan)  # Cambiar el user_id según sea necesario

        # Verificar si hubo error en la generación del plan
        if "error" in diet_plan:
            raise HTTPException(status_code=500, detail=f"Error generando el plan alimenticio: {diet_plan['error']}")
        
        # Retornar ambos resultados
        return {
            "transcript": transcript,
            "diet_plan": diet_plan,
            "status": "success"
        }
        
    except HTTPException as he:
        raise he
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
@router.get("/nutrition-plan/{google_id}", response_model=DietPlanResponse)
async def get_nutrition_plan_by_google_id(
    google_id: str,
    db: Session = Depends(get_db)
):
    try:
        # Buscar usuario por google_id
        user = db.query(User).filter(User.google_id == google_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Obtener el plan más reciente del usuario
        diet_plan = db.query(DietPlan).filter(DietPlan.user_id == user.id).order_by(DietPlan.id.desc()).first()

        if not diet_plan:
            raise HTTPException(status_code=404, detail="Plan nutricional no encontrado")

        return diet_plan

    except Exception as e:
        logger.error(f"Error obteniendo plan nutricional: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener el plan nutricional")

# # Obtener un plan de dieta por su id
# @router.get("/diet-plan/{diet_plan_id}", response_model=DietPlanResponse)
# async def get_diet_plan(diet_plan_id: int, db: Session = Depends(get_db)):
#     try:
#         # Obtener un plan de dieta por su ID
#         diet_plan = db.query(DietPlan).filter(DietPlan.id == diet_plan_id).first()
#         if not diet_plan:
#             raise HTTPException(status_code=404, detail="Plan de dieta no encontrado.")
#         return diet_plan
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error obteniendo el plan de dieta: {str(e)}")
@router.post("/regenerate-nutrition-plan/{google_id}", response_model=DietPlanResponse)
async def regenerate_nutrition_plan(google_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar usuario por google_id
        user = db.query(User).filter(User.google_id == google_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Obtener el plan más reciente del usuario
        diet_plan = db.query(DietPlan).filter(DietPlan.user_id == user.id).order_by(DietPlan.id.desc()).first()
        
        if not diet_plan:
            raise HTTPException(status_code=404, detail="Plan nutricional no encontrado")
        
        # Generar un nuevo plan basado en los objetivos del usuario (usando `get_diet_plan`)
        objectives = "Objetivos del usuario aquí"  # Esto debe ser recuperado según el caso
        new_diet_plan = get_diet_plan(objectives)  # Llama a tu función para obtener el nuevo plan

        # Verificar si se generó un plan válido
        if "error" in new_diet_plan:
            raise HTTPException(status_code=500, detail="Error regenerando el plan nutricional")
        
        # Actualizar el plan en la base de datos
        diet_plan.plan = json.dumps(new_diet_plan, ensure_ascii=False)  # Actualiza el plan
        db.commit()
        db.refresh(diet_plan)  # Recarga el objeto actualizado
        
        return diet_plan  # Devuelve el plan actualizado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al regenerar el plan nutricional: {str(e)}")