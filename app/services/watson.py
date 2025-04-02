import requests
import os

# Cargar las claves y URLs desde las variables de entorno
STT_API_KEY = "bVFrRyp5cmzf2kyS0mTP_r6i7n5kU3qXWegSnJGi8bVP"
STT_URL = "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/581628eb-be46-4f10-9f61-fba5065fe244"

TTS_API_KEY = "OgOJwJKXN9SDEcZAIXoSz1WZjom5gL3WTeB4IDZlLRsH"
TTS_URL = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/762ea9cf-aefd-45b9-9fa2-2106704f5725"


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