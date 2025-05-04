import os
from openai import OpenAI
import base64
from dotenv import load_dotenv

# Configuración del cliente
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def encode_image(image_path):
    """Codifica la imagen en base64 para enviarla a la API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_machine(image_path):
    prompt = (
         "Eres un asistente que responde exclusivamente en español. No incluyas texto fuera del JSON solicitado."
        "Analiza la imagen de la máquina de ejercicio. "
        "Si la imagen no es de una máquina de ejercicio o es irreconocible (por ejemplo, si es una pared, un objeto que no parece una máquina, o una imagen que no puede ser identificada), "
        "debe devolver un JSON con la clave 'error' y el valor 'No es una máquina de ejercicio'. "
        "Si la imagen corresponde a una máquina de ejercicio, devuelve un JSON con las siguientes claves y valores: "
        '{ '
        '"nombre_maquina": "Nombre completo de la máquina de ejercicio (por ejemplo, Banco de Peso, Bicicleta Estática, Máquina de Prensa de Piernas)", '
        '"uso": "Descripción corta sobre el ejercicio o tipo de entrenamiento que se realiza con la máquina (por ejemplo, Ejercicios para pecho, Cardio de bajo impacto, Ejercicios de pierna)", '
        '"riesgo": "Nivel de riesgo asociado con el uso de la máquina (bajo, medio, alto). El riesgo puede depender de la complejidad del ejercicio o el potencial de lesión (por ejemplo, \'alto\' para máquinas de levantamiento de pesas sin supervisión, \'bajo\' para máquinas de cardio como bicicletas estáticas)", '
        '"series_recomendadas": "Número de series recomendadas para el ejercicio (por ejemplo, 3-4 series de 10 repeticiones)", '
        '"musculos_trabajados": "Lista completa de músculos principales y secundarios trabajados por la máquina. Enuméralos todos de manera breve, separados por comas. Por ejemplo: Pecho, Tríceps, Hombros, Core.", '
        '"descripcion": "La descripción debe ser detallada y tener al menos 2-3 frases completas que expliquen el diseño de la máquina, su propósito, y cómo se utiliza típicamente en un entorno de entrenamiento. Usa un lenguaje claro y técnico.", '
        '"estado": "Si la máquina parece estar en mal estado o incompleta, devuelve el valor \'dañada\' o \'incompleta\' dependiendo de lo que veas (por ejemplo, si hay piezas rotas o faltantes, o si la máquina no tiene parte de su estructura). Si no hay indicios de daño, simplemente omite este campo.", '
        '} '
        "Si alguno de los valores no puede determinarse con certeza, devuelve 'null' para esa clave, pero no dejes claves vacías. "
        "Si la imagen no corresponde a una máquina de ejercicio, no contiene una máquina visible, o es imposible de identificar, asegúrate de que la respuesta sea un JSON bien formado que incluya solo la clave 'error' con el valor correspondiente. "
        "No escribas nada más fuera del JSON. "
        "Por ejemplo, una salida válida podría ser: "
        '{ '
        '"nombre_maquina": "", '
        '"uso": "", '
        '"riesgo": "", '
        '"series_recomendadas": "", '
        '"musculos_trabajados": "", '
        '"descripcion": "", '
        '"estado": "" '
        '}'
    )
    """Envía la imagen de la máquina y el prompt a Together AI"""
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
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error al llamar a la API: {e}")
        return None