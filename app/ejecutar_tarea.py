import requests

def marcar_no_registrado():
    url = "http://127.0.0.1:8000/run_background_task"  # Asegúrate de que esta es la URL correcta
    response = requests.post(url)
    print(f"Respuesta de la API: {response.status_code}")

if __name__ == "__main__":
    marcar_no_registrado()
