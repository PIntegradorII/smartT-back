import json
import re
import os
from dotenv import load_dotenv
from together import Together

from app.schemas.physical import PhysicalDataCreate

load_dotenv()

# Inicializar cliente con la API Key de Together
api_key = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=api_key)

# Lista de ejercicios permitidos
EJERCICIOS_VALIDOS = [
    "3/4 sit-up", "air bike", "barbell press sit-up",
    "assisted pull-up", "barbell pullover", "cable bar lateral pulldown",
    "barbell bench press", "cable cross-over variation", "barbell incline bench press",
    "barbell straight leg deadlift", "dumbbell lying femoral", "lever lying leg curl",
    "barbell close-grip bench press", "barbell lying triceps extension skull crusher", "assisted triceps dip (kneeling)",
    "barbell squat (on knees)", "barbell bench squat", "barbell overhead squat",
    "barbell curl", "barbell preacher curl", "barbell drag curl",
    "barbell bent over row", "cable low seated row", "cable high row (kneeling)",
    "barbell deadlift", "barbell front squat", "barbell lunge",
    "barbell front raise", "barbell rear delt raise", "barbell seated overhead press"
]

# Plantilla de entrenamiento en formato JSON
JSON_TEMPLATE = {
    "lunes": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "martes": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "miercoles": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "jueves": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]},
    "viernes": {"titulo": "", "musculos": [], "ejercicios": [{"ejercicio": "", "series": 0, "repeticiones": ""}]}
}

def chat_with_model(user_data):
    """Envía los datos del usuario a la IA y obtiene el plan de entrenamiento"""
    ejercicios_lista = json.dumps(EJERCICIOS_VALIDOS, indent=2)

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
                f"Instrucciones importantes:\n"
                f"1. Usa **únicamente** los ejercicios contenidos en la siguiente lista.\n"
                f"2. El nombre del ejercicio debe coincidir exactamente con los nombres de esta lista (sin traducciones, sin combinaciones, sin variaciones).\n"
                f"Lista de ejercicios permitidos:\n{ejercicios_lista}\n\n"
                f"Minimo requiero 5 ejercicios por día.\n"
                f"Formato de salida requerido (estructura JSON):\n{json.dumps(JSON_TEMPLATE, indent=2)}\n"
                f"Devuelve únicamente el JSON como respuesta. No incluyas explicaciones, encabezados, ni texto adicional."
            )
        }
    ]


    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=chat_history
    )

    return response.choices[0].message.content

def extraer_json(texto):
    """Extrae un JSON contenido en un string de la respuesta de la IA"""
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
    """Genera el plan de entrenamiento basado en los datos proporcionados por el usuario"""
    respuesta_ia = chat_with_model(user_data)
    return extraer_json(respuesta_ia)



def modificar_rutina_dia(dia, rutina_actual):
    """ Modifica la rutina de un día específico manteniendo el grupo muscular """
    ejercicios_lista = json.dumps(EJERCICIOS_VALIDOS, indent=2)
    chat_history = [
        {
            "role": "user",
            "content": (
                f"Eres un entrenador de gimnasio experto. Necesito modificar la rutina de entrenamiento del {dia}. "
                f"Conserva el mismo grupo de músculos pero cambia los ejercicios y sus repeticiones.\n"
                f"Aquí está la rutina actual:\n"
                f"{json.dumps(rutina_actual, indent=2)}\n"
                f"Instrucciones importantes:\n"
                f"1. Usa **únicamente** los ejercicios contenidos en la siguiente lista.\n"
                f"2. El nombre del ejercicio debe coincidir exactamente con los nombres de esta lista (sin traducciones, sin combinaciones, sin variaciones).\n"
                f"Lista de ejercicios permitidos:\n{ejercicios_lista}\n\n"
                f"Minimo requiero 5 ejercicios por día.\n"
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


def analizar_progreso_fisico(current_data: PhysicalDataCreate, historial: list, pregunta_usuario: str):
    """
    Analiza el progreso físico del usuario en función de sus datos actuales y el historial reciente.
    Devuelve una respuesta breve (2-3 líneas) centrada en cambios importantes.
    Si la pregunta no tiene relación con el progreso físico, lo indica.
    """

    prompt = (
        "Eres un entrenador personal experto. Analiza de forma concisa el progreso físico de un usuario "
        "comparando sus medidas actuales con las anteriores. Responde en 2 o 3 líneas máximo, usando lenguaje claro y directo. "
        "Menciona si hubo mejoras o retrocesos en medidas clave (peso, IMC, cintura, etc.). No des explicaciones largas.\n\n"
        "Si la pregunta no tiene relación con fitness o progreso físico, responde: "
        "'Tu pregunta no está relacionada con tu progreso físico, no puedo responder eso.'\n\n"
    )

    mensaje = prompt
    mensaje += "📊 Medidas actuales:\n"
    mensaje += f"- Peso: {current_data.peso} kg, IMC: {current_data.imc}, Cintura: {current_data.cintura} cm, Objetivo: {current_data.objetivo}\n\n"

    if historial:
        last = historial[-1]
        mensaje += "📉 Último registro anterior:\n"
        mensaje += f"- Peso: {last.peso} kg, IMC: {last.imc}, Cintura: {last.cintura} cm, Objetivo: {last.objetivo} (Fecha: {last.created_at.date()})\n\n"

    mensaje += f"❓ Pregunta del usuario: \"{pregunta_usuario}\"\n"

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=[{"role": "user", "content": mensaje}]
    )

    return response.choices[0].message.content.strip()
