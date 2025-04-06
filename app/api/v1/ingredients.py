from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from app.services.recipe_service import get_recipe_from_ingredients, save_or_update_recipe
from app.schemas.receta import RecipeRequest
from app.db.database import Session, get_db
from app.models.user import User
from app.services.watson import speech_to_text

router = APIRouter()

@router.post("/voice-to-recipes")
async def voice_to_text(
    google_id: str = Form(...),  # Usar Form para google_id
    audio: UploadFile = File(...),  # Usar File para el archivo de audio
    db: Session = Depends(get_db)  # Dependencia para obtener la sesión de la base de datos
):
    """
    Convierte entrada de audio a texto y genera una receta.
    :param audio: Archivo de audio subido.
    :param google_id: El google_id del usuario.
    :return: Receta generada en formato JSON.
    """
    try:
        # Leer el archivo de audio
        audio_bytes = await audio.read()
  
        # Determinar el tipo de contenido basado en el nombre del archivo
        content_type = "audio/wav" if audio.filename.endswith(".wav") else audio.content_type
        print(f"Tipo de contenido: {content_type}")

        # Convertir de audio a texto
        transcript = speech_to_text(audio_bytes, content_type=content_type)
        print("transcript", transcript)
        
        #transcript = """ cebolla, ajo, aceite de oliva, sal, pimienta, pollo. """
        # Llamar a la API de recetas con los ingredientes transcritos
        
        recipe = get_recipe_from_ingredients(transcript)
        print("recipe", recipe)
        # Buscar al usuario por su google_id
        user = db.query(User).filter(User.google_id == google_id).first()
        print("user", user)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        print(user.id, transcript, recipe)
        # Guardar o actualizar la receta
        save_or_update_recipe(user.id, transcript, recipe)
        print("Receta guardada o actualizada correctamente", save_or_update_recipe)
        # Devolver la receta generada y la transcripción del audio
        return {"transcript": transcript, "recipe": recipe}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento: {str(e)}")
