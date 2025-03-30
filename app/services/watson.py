import requests
import os

# Cargar las claves y URLs desde las variables de entorno
STT_API_KEY = os.getenv("IBM_STT_API_KEY")
STT_URL = os.getenv("IBM_STT_URL")
TTS_API_KEY = os.getenv("IBM_TTS_API_KEY")
TTS_URL = os.getenv("IBM_TTS_URL")

def speech_to_text(audio_file: bytes, content_type="audio/wav"):
    """
    Convierte audio a texto usando IBM Watson Speech to Text en español.
    :param audio_file: Archivo de audio en formato binario.
    :param content_type: Tipo de contenido del archivo (e.g., "audio/wav").
    :return: Texto transcrito.
    """
    headers = {
        "Content-Type": content_type,
    }
    auth = ("apikey", STT_API_KEY)
    try:
        # Agregar el modelo de español en la URL
        response = requests.post(
            f"{STT_URL}/v1/recognize?model=es-ES_BroadbandModel",
            headers=headers,
            data=audio_file,
            auth=auth
        )
        response.raise_for_status()  # Lanza una excepción para errores HTTP
        json_response = response.json()

        # Validar que la respuesta contiene resultados
        if "results" in json_response and len(json_response["results"]) > 0:
            return json_response["results"][0]["alternatives"][0]["transcript"]
        else:
            raise Exception("No se encontraron resultados en la respuesta de Watson Speech to Text.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error en la solicitud HTTP: {e}")
    except ValueError as e:
        raise Exception(f"Error al decodificar la respuesta JSON: {e}")

