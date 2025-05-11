from fastapi import APIRouter, HTTPException, File, UploadFile
import uuid
import os
import json
from PIL import Image
import numpy as np
from dotenv import load_dotenv
import base64
from openai import OpenAI

# Configuración del cliente OpenAI
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

router = APIRouter()

# Función para verificar si la imagen es completamente negra
def is_image_black(image_path):
    """Verifica si la imagen es completamente negra"""
    with Image.open(image_path) as img:
        img_gray = img.convert('L')
        img_array = np.array(img_gray)
        if np.all(img_array == 0):
            return True
    return False

# Codificar imagen en base64
def encode_image(image_path):
    """Codifica la imagen en base64 para enviarla a la API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Llamar a Meta LLaMA Vision Free para análisis del plato
def analyze_food(image_path):
    """Realiza el análisis del plato a través de Meta LLaMA Vision Free"""
    prompt = (
        "Eres un asistente que responde exclusivamente en español. No incluyas texto fuera del JSON solicitado. "
        "Analiza la imagen de un plato de comida. "
        "Si la imagen no corresponde a un plato de comida o es irreconocible (por ejemplo, si es una foto de un objeto, una pared o algo que no es comida), "
        "devuelve únicamente un JSON con la clave 'error' y el valor 'Imagen no válida'. "
        "Si la imagen corresponde a un plato de comida, devuelve un JSON bien formado con el siguiente formato: "
        "{ "
        '"nombre_plato": "Nombre común del plato (por ejemplo, Ensalada César, Pollo asado con arroz)", '
        '"calorias": "Calorías totales estimadas del plato en números enteros", '
        '"macronutrientes": { '
        '"proteinas": "Cantidad estimada en gramos de proteínas como número entero", '
        '"grasas": "Cantidad estimada en gramos de grasas como número entero", '
        '"carbohidratos": "Cantidad estimada en gramos de carbohidratos como número entero" '
        '}, '
        '"ingredientes": ["Lista de ingredientes principales del plato como strings"] '
        "}. "
        "No escribas ningún texto adicional fuera del JSON, ni explicaciones, ni comentarios. "
        "Si tienes dudas sobre algún valor, devuelve 'null' para esa clave. "
        "Por ejemplo, una salida válida podría ser: "
        '{ '
        '"nombre_plato": "Ensalada César", '
        '"calorias": 250, '
        '"macronutrientes": { '
        '"proteinas": 10, '
        '"grasas": 20, '
        '"carbohidratos": 5 '
        '}, '
        '"ingredientes": ["lechuga", "pollo", "queso parmesano", "crutones", "aderezo César"] '
        '}.'
    )   

    base64_image = encode_image(image_path)

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error al llamar a la API: {e}")
        return None