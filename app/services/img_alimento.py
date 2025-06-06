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
def identify_food_items(image_path):
    """
    Analiza la imagen y devuelve información nutricional y descriptiva de cada alimento identificado.
    Si no se reconoce ningún alimento, devuelve {"error": "Imagen no válida"}.
    """
    prompt = (
        "Eres un asistente que responde exclusivamente en español. No incluyas texto fuera del JSON solicitado. "
        "Analiza la imagen y detecta alimentos visibles. "
        "Si la imagen no corresponde a alimentos (por ejemplo, si es una foto de una pared, una persona o un objeto no comestible), "
        "devuelve únicamente: {\"error\": \"Imagen no válida\"}. "
        "Si es más de un alimento entonces devuelvo descripciones y los demás campos pero cortos, no des mucho detalle o texto."
        "Si es más de un alimento, de la imagen seleciona como maximo 5 alimentos. UNICAMENTE 5 ALIMENTOS COMO MAXIMO. NUNCA DES MÁS DE 5 ALIMENTOS. "
        "Si hay uno o varios alimentos, devuelve un JSON en el siguiente formato y sólamente el JSON: "
        "{ "
        "\"alimentos\": [ "
        "{ "
        "\"nombre\": \"Nombre común del alimento (por ejemplo, Manzana, Zanahoria, Huevo cocido)\", "
        "\"calorias\": Número entero estimado de calorías, "
        "\"beneficios\": \"Descripción corta de beneficios para la salud\", "
        "\"contraindicaciones\": \"Advertencias o posibles riesgos si existen (si no hay, escribe 'Ninguna conocida')\", "
        "\"descripcion\": \"Breve descripción del alimento\" "
        "} "
        "(repite este bloque por cada alimento identificado en la imagen) "
        "] "
        "}. "
        "No escribas ningún texto adicional fuera del JSON, ni explicaciones, ni comentarios. "
        "Si tienes dudas sobre algún valor, devuelve 'null' para esa clave. "
        "Ejemplo de respuesta válida: "
        "{ "
        "\"alimentos\": [ "
        "{ "
        "\"nombre\": \"Manzana\", "
        "\"calorias\": 52, "
        "\"beneficios\": \"Rica en fibra y vitamina C, ayuda a la digestión.\", "
        "\"contraindicaciones\": \"Evitar en exceso si hay intolerancia a la fructosa.\", "
        "\"descripcion\": \"Fruta dulce y jugosa, comúnmente de color rojo, verde o amarillo.\" "
        "} "
        "] "
        "}"
    )
    # Aquí iría la llamada al modelo de visión, pasando el `prompt` y la `image_path`
   

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
            max_tokens=4096,
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error al llamar a la API: {e}")
        return None