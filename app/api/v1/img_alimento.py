from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.img_maquinas import ImgMaquinaSchema
from app.services.img_alimento import identify_food_items, is_image_black
import uuid
import os
import json
import re
from PIL import Image
import numpy as np
router = APIRouter()
@router.post("/identify_food_items")
async def identify_food_items_endpoint(file: UploadFile = File(...)):
    """Endpoint para analizar un plato de comida"""
    os.makedirs("foodIMG/uploads", exist_ok=True)
    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join("foodIMG/uploads", image_filename)

    try:
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {e}")

    # Validar que la imagen no esté completamente negra
    if is_image_black(image_path):
        raise HTTPException(status_code=400, detail="La imagen está vacía o es completamente negra.")

    # Llamar a la función de análisis
    result_text = identify_food_items(image_path)

    if not result_text:
        raise HTTPException(status_code=500, detail="No se pudo procesar la imagen.")
    print(result_text)
    #Extraer el JSON desde el texto
    # try:
    #     result_json = json.loads(result_text)
    # except json.JSONDecodeError:
    #     raise HTTPException(status_code=400, detail="El bloque extraído no es un JSON válido.")
    
    try:
        result_json = extract_json_block(result_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="El bloque extraído no es un JSON válido. " + str(e))

    # Validar si el análisis fue exitoso
    if "error" in result_json:
        raise HTTPException(status_code=400, detail=result_json["error"])

    # Devolver el análisis del plato
    return result_json


def extract_json_block(text: str) -> dict:
    """
    Extrae, limpia y valida un bloque JSON con clave 'alimentos' desde texto.
    Maneja errores comunes como comas finales o cortes por límite de tokens.
    """
    json_pattern = re.compile(r'\{[\s\S]*?"alimentos"\s*:\s*\[.*?\][\s\S]*?\}', re.DOTALL)
    match = json_pattern.search(text)

    if not match:
        raise ValueError("No se encontró un bloque JSON con la clave 'alimentos'.")

    json_str = match.group(0)

    # Eliminar comas finales antes de cerrar objetos en la lista
    json_str = re.sub(r',\s*([\]}])', r'\1', json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"El bloque extraído no es un JSON válido: {e}")
