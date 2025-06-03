from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Dict
import os
import uuid
import requests
from PIL import Image
from pyzbar.pyzbar import decode
from app.services.barcode_service import analizar_alimento_con_objetivo

router = APIRouter()

def filtrar_analisis_ia(texto: str) -> str:
    """
    Elimina bloques tipo <think> o contenido irrelevante generado por el modelo.
    """
    import re
    texto_filtrado = re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL)
    lineas = [line.strip() for line in texto_filtrado.strip().split("\n") if line.strip()]
    return "\n".join(lineas[:3])

@router.post("/escaneo-nutricional")
async def escaneo_nutricional(
    file: UploadFile = File(...),
    objetivo: str = Form(None)
) -> Dict:
    os.makedirs("nutricionIMG/uploads", exist_ok=True)
    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join("nutricionIMG/uploads", image_filename)

    try:
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {e}")

    try:
        img = Image.open(image_path)
        decoded = decode(img)
        if not decoded:
            raise HTTPException(status_code=400, detail="No se detectó ningún código de barras en la imagen. Intenta con otra foto.")
        codigo_barras = decoded[0].data.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el Barcode: {e}")

    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{codigo_barras}.json"
        response = requests.get(url)
        data = response.json()

        if data.get("status") != 1:
            raise HTTPException(status_code=404, detail="Este alimento no se encuentra en la base de datos de Open Food Facts.")
        producto = data["product"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar Open Food Facts: {e}")

    nutr = producto.get("nutriments", {})
    resumen = {
        "producto": producto.get("product_name", "Desconocido"),
        "calorias_kcal_100g": nutr.get("energy-kcal_100g", "N/A"),
        "grasas_g": nutr.get("fat_100g", "N/A"),
        "azucares_g": nutr.get("sugars_100g", "N/A"),
        "proteinas_g": nutr.get("proteins_100g", "N/A"),
        "sal_g": nutr.get("salt_100g", "N/A")
    }

    analisis_ia = None
    if objetivo:
        try:
            raw_analisis = analizar_alimento_con_objetivo(objetivo, resumen)
            analisis_ia = filtrar_analisis_ia(raw_analisis)
        except Exception:
            analisis_ia = "El agente de IA no está disponible en este momento."

    return {
        "codigo_barras": codigo_barras,
        "producto": producto.get("product_name", "Desconocido"),
        "nutrientes": nutr,
        "resumen": resumen,
        "analisis_ia": analisis_ia
    }
