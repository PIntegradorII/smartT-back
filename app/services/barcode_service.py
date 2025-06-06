import json
import os
import re
from dotenv import load_dotenv
from together import Together

load_dotenv()

# Inicializar cliente con la API Key de Together
api_key = os.getenv("TOGETHER_API_KEY_2")
client = Together(api_key=api_key)

def analizar_alimento_con_objetivo(meta_usuario: str, resumen: dict) -> str:

    prompt = f"""
    Eres un nutricionista profesional. Tu tarea es analizar si un alimento es adecuado o no
    para la meta nutricional de una persona.

    ### Objetivo del usuario:
    {meta_usuario}

    ### Información del alimento (por cada 100g):
    - Calorías: {resumen.get("calorias_kcal_100g", "N/A")} kcal
    - Grasas: {resumen.get("grasas_g", "N/A")} g
    - Azúcares: {resumen.get("azucares_g", "N/A")} g
    - Proteínas: {resumen.get("proteinas_g", "N/A")} g
    - Sal: {resumen.get("sal_g", "N/A")} g

    ### Instrucciones:
    Redacta una respuesta en el siguiente formato:
    "Teniendo en cuenta que tu objetivo es {meta_usuario}, y este alimento contiene [resumen nutricional], entonces [evaluación]."
    - Sustituye [resumen nutricional] por un resumen breve basado en los valores.
    - Sustituye [evaluación] por una recomendación corta.
    - Usa un lenguaje claro, directo y amigable.
    - Máximo 3 líneas. Solo texto plano.

    """

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
