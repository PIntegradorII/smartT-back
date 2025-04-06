import requests
import os

# Cargar las claves y URLs desde las variables de entorno
STT_API_KEY = os.getenv("IBM_STT_API_KEY")
STT_URL = os.getenv("IBM_STT_URL")
TTS_API_KEY = os.getenv("IBM_TTS_API_KEY")
TTS_URL = os.getenv("IBM_TTS_URL")

def speech_to_text(audio_file: bytes, content_type="audio/wav"):
    headers = {
        "Content-Type": content_type,
    }
    auth = ("apikey", STT_API_KEY)
    print("sqiiiiii")
    try:
       
        print("datosss", headers)
        response = requests.post(
            f"{STT_URL}/v1/recognize?model=es-ES_BroadbandModel",
            headers=headers,
            data=audio_file,
            auth=auth
        )
        print(f"Respuesta de Watson: {response.status_code} {response.text}")
        response.raise_for_status()  # Lanzar error si no es 2xx

        json_response = response.json()
        if "results" in json_response and len(json_response["results"]) > 0:
            return json_response["results"][0]["alternatives"][0]["transcript"]
        else:
            raise Exception("Sin resultados de transcripción en la respuesta.")
    except requests.exceptions.RequestException as req_error:
        print(f"Error en la solicitud a Watson: {req_error}")
        raise Exception(f"Error en la solicitud a Watson: {req_error}")
    except Exception as e:
        print(f"Error general en Watson: {e}")
        raise Exception(f"Error en Watson: {e}")
