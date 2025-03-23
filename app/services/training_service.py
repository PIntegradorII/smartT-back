
import json
import re
import os
from dotenv import load_dotenv
from together import Together

load_dotenv()

# Inicializar cliente con la API Key de Together
api_key = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=api_key)

# Datos estáticos del usuario (serán extraídos de la BD en el futuro)
# USER_DATA = {
#     "nombre": "Juan Pérez",
#     "peso": 75,  # kg
#     "altura": 1.75,  # m
#     "sexo": "Masculino",
#     "condiciones_medicas": ["Ninguna"],
#     "meta_entrenamiento": "Aumentar masa muscular"
# }

# Plantilla de entrenamiento en JSON
JSON_TEMPLATE = {
    "lunes": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "martes": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "miercoles": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "jueves": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "viernes": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]}
}

def chat_with_model(user_data):
    """ Envía los datos del usuario a la IA y obtiene el plan de entrenamiento """
    chat_history = [
        {
            "role": "user",
            "content": (
                f"Eres un entrenador de gimnasio experto. Genera planes de entrenamiento en formato JSON "
                f"personalizados según los datos del usuario.\n\n"
                f"Datos del usuario:\n"
                f"- Nombre: {user_data['nombre']}\n"
                f"- Peso: {user_data['peso']} kg\n"
                f"- Altura: {user_data['altura']} m\n"
                f"- Sexo: {user_data['sexo']}\n"
                f"- Condiciones médicas: {', '.join(user_data['condiciones_medicas'])}\n"
                f"- Meta del entrenamiento: {user_data['meta_entrenamiento']}\n\n"
                f"Usa la siguiente estructura:\n\n{json.dumps(JSON_TEMPLATE, indent=2)}"
                f"Dame la salida en formato JSON, por favor."
            )
        }
    ]

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=chat_history
    )

    return response.choices[0].message.content

def extraer_json(texto):
    """ Extrae un JSON contenido en un string de la respuesta de la IA """
    patron_json = r"```json\n(.*?)\n```"
    coincidencia = re.search(patron_json, texto, re.DOTALL)

    if coincidencia:
        try:
            return json.loads(coincidencia.group(1))
        except json.JSONDecodeError:
            print("Error: El JSON extraído no es válido.")
            return None
    else:
        print("No se encontró JSON en el texto.")
        return None

def generar_plan_entrenamiento(user_data):
    """ Genera el plan de entrenamiento basado en los datos proporcionados por el usuario """
    respuesta_ia = chat_with_model(user_data)
    return extraer_json(respuesta_ia)



def modificar_rutina_dia(dia, rutina_actual):
    """ Modifica la rutina de un día específico manteniendo el grupo muscular """
    
    chat_history = [
        {
            "role": "user",
            "content": (
                f"Eres un entrenador de gimnasio experto. Necesito modificar la rutina de entrenamiento del {dia}. "
                f"Conserva el mismo grupo de músculos pero cambia los ejercicios y sus repeticiones.\n"
                f"Aquí está la rutina actual:\n"
                f"{json.dumps(rutina_actual, indent=2)}\n"
                f"Devuélveme el resultado en este mismo formato JSON, solo con los ejercicios y repeticiones modificados."
            )
        }
    ]
    
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=chat_history
    )
    
    nueva_rutina = extraer_json(response.choices[0].message.content)
    
    return nueva_rutina if nueva_rutina else rutina_actual  # Si falla, devolver la rutina original



