from fastapi import APIRouter, File, UploadFile, HTTPException
import requests
import os
from app.services.watson import speech_to_text
# Cargar las claves y URLs desde las variables de entorno
STT_API_KEY = os.getenv("IBM_STT_API_KEY")
STT_URL = os.getenv("IBM_STT_URL")

router = APIRouter()



@router.post("/voice-to-text")
async def voice_to_text(audio: UploadFile = File(...)):
    """
    Convierte entrada de audio a texto en español.
    :param audio: Archivo de audio subido.
    :return: Texto transcrito.
    """
    try:
        # Leer el archivo de audio
        audio_bytes = await audio.read()

        # Determinar el tipo de contenido basado en el nombre del archivo
        content_type = "audio/wav" if audio.filename.endswith(".wav") else audio.content_type

        # Convertir de audio a texto
        transcript = speech_to_text(audio_bytes, content_type=content_type)

        # Responder con el texto transcrito
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento: {str(e)}")