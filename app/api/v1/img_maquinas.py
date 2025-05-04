from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.img_maquinas import ImgMaquinaSchema
from app.services.img_maquinas import analyze_machine
from app.models.img_maquinas import ImgMaquina
import uuid
import os
import json
import re
from PIL import Image
import numpy as np

router = APIRouter()

# Función para verificar si la imagen es completamente negra
def is_image_black(image_path):
    """Verifica si la imagen es completamente negra"""
    with Image.open(image_path) as img:
        # Convertir la imagen a escala de grises
        img_gray = img.convert('L')
        img_array = np.array(img_gray)
        
        # Verificar si todos los píxeles son 0 (negro)
        if np.all(img_array == 0):
            return True
    return False

# Función para validar la respuesta de la API
def validate_machine_analysis(result_json):
    """Valida que el análisis de la máquina sea correcto"""
    # Si la respuesta tiene una clave 'error', la rechazamos directamente
    if "error" in result_json:
        raise HTTPException(status_code=400, detail="No se identificó una máquina de ejercicio en la imagen.")

    # Si no hay nombre de máquina, o si los campos esenciales están vacíos o sospechosos
    campos_esperados = ["nombre_maquina", "uso", "descripcion"]
    for campo in campos_esperados:
        if campo not in result_json or not result_json[campo].strip():
            raise HTTPException(status_code=400, detail="La imagen no contiene una máquina de ejercicio válida.")
        
    # Adicionalmente, podrías verificar que el nombre de la máquina no sea algo sospechoso
    nombre = result_json["nombre_maquina"].lower()
    if "máquina" not in nombre and "banco" not in nombre and "bicicleta" not in nombre:
        raise HTTPException(status_code=400, detail="No se reconoció una máquina de ejercicio válida.")


@router.post("/scan", response_model=ImgMaquinaSchema)
async def scan_machine(
    google_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs("maquinasIMG/uploads", exist_ok=True)  # Corregido el path para evitar errores en Linux/Mac

    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join("maquinasIMG/uploads", image_filename)

    try:
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {e}")

    # ✅ Validar que la imagen no esté completamente negra
    if is_image_black(image_path):
        raise HTTPException(status_code=400, detail="La imagen está vacía o es completamente negra.")

    # ✅ Llamar a la API de análisis
    result_text = analyze_machine(image_path)

    if not result_text:
        raise HTTPException(status_code=500, detail="No se pudo procesar la imagen.")

    # ✅ Extraer el JSON desde el texto (usando expresión regular)
    match = re.search(r'\{.*\}', result_text, re.DOTALL)
    if not match:
        raise HTTPException(status_code=400, detail="No se encontró un bloque JSON en la respuesta del análisis.")

    try:
        result_json = json.loads(match.group())
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="El bloque extraído no es un JSON válido.")

    # ✅ Validar que el análisis sí corresponda a una máquina de ejercicio
    validate_machine_analysis(result_json)

    # ✅ Verificar existencia del usuario
    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # ✅ Guardar la imagen y los datos de análisis
    img_maquina = ImgMaquina(
        user_id=user.id,
        maquina_data=result_json,
        image_path=image_path
    )

    try:
        db.add(img_maquina)
        db.commit()
        db.refresh(img_maquina)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {e}")

    return img_maquina
