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
import re  # 👈 necesario para extraer el JSON del texto

router = APIRouter()

@router.post("/scan", response_model=ImgMaquinaSchema)
async def scan_machine(
    google_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs("uploads", exist_ok=True)

    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join("uploads", image_filename)

    try:
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
        print(f"Imagen guardada en: {image_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {e}")

    result_text = analyze_machine(image_path)

    if not result_text:
        raise HTTPException(status_code=500, detail="No se pudo procesar la imagen.")

    # 🧠 Extraer solo el JSON del texto devuelto por la API
    match = re.search(r'\{.*\}', result_text, re.DOTALL)
    if not match:
        print("❌ No se encontró JSON en la respuesta:")
        print(result_text)
        raise HTTPException(status_code=500, detail="No se pudo extraer un JSON válido del resultado.")

    try:
        result_json = json.loads(match.group())
    except json.JSONDecodeError:
        print("❌ JSON extraído no es válido:")
        print(match.group())
        raise HTTPException(status_code=500, detail="El bloque extraído no es un JSON válido.")

    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    img_maquina = ImgMaquina(
        user_id=user.id,
        maquina_data=result_json,  # ✅ Se guarda como dict, no string
        image_path=image_path
    )

    try:
        db.add(img_maquina)
        db.commit()
        db.refresh(img_maquina)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {e}")

    return img_maquina
