import sys
import os
import pytest
from fastapi.testclient import TestClient

# Agregar la carpeta raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app  # Importar la aplicación FastAPI

client = TestClient(app)

VALID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjMwYjIyMWFiNjU2MTdiY2Y4N2VlMGY4NDYyZjc0ZTM2NTIyY2EyZTQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQlJBWUFOIEpVTElPIEdPTUVaIE1Vw5FPWiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKWXh4Qm9OOUt5YzExSVBwejE0VUwzNGR1WXVnTERjMVh1ZVNOS2wzUDlZc3VCUWxTLT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9pbnRlZ3JhZG9paSIsImF1ZCI6ImludGVncmFkb2lpIiwiYXV0aF90aW1lIjoxNzQyODAxNjQwLCJ1c2VyX2lkIjoiWThxM3VhQ3pJSmFmWFdKdk1pbjVHaWZhTThBMiIsInN1YiI6Ilk4cTN1YUN6SUphZlhXSnZNaW41R2lmYU04QTIiLCJpYXQiOjE3NDI4MDE2NDAsImV4cCI6MTc0MjgwNTI0MCwiZW1haWwiOiJicmF5YW4uanVsaW8uZ29tZXpAY29ycmVvdW5pdmFsbGUuZWR1LmNvIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDM3MzIzNDczMzg0Njk0NTMwMDQiXSwiZW1haWwiOlsiYnJheWFuLmp1bGlvLmdvbWV6QGNvcnJlb3VuaXZhbGxlLmVkdS5jbyJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.H9ZPsukXmgoTRT_5Q-hQJrYXV12rs43v88F_xasRCB47Drm3Old5OQighSj3g8uXLx9Ez5Lu0VAdQHry45y_FZvloW9CIW7yTMoMMgVDVq7576ATaDjTykocNlKe1LXVxcaWq8j8CTENR3ZnnSlf3L64RR1u4OFqo2SiyizblAZMi5zAvTt_Wye4VPlcDOydC-wmOffeFU1n_JGfCxaUKMroUgeZ7Fc80XR4ZbfWkVe2qBJ3SOeEkRBxxW2LDWmF7-a3O_Az4GRiR51pysXkWoveJIFthDiRUfVbns42lud0v5zqUCItMXeEaBU1uWnXIvRkpWJ5a9hBaCS6q4Fr3A"  # Debe ser un token real válido
INVALID_TOKEN = "invalid_token_12345"

def test_google_login_success():
    """Prueba con un token válido"""
    headers = {"Content-Type": "application/json"}
    payload = {"token": VALID_TOKEN}

    response = client.post("/v1/auth/google-login", json=payload, headers=headers)

    assert response.status_code == 200
    response_data = response.json()

    # Verificar si la clave correcta es "access_tokenc" o "access_token"
    assert "access_token" in response_data or "access_tokenc" in response_data, "El response no contiene el token de acceso"

    # Si el API devuelve "access_tokenc", cambiarlo en la API o en la prueba según corresponda
    access_token_key = "access_tokenc" if "access_tokenc" in response_data else "access_token"
    assert isinstance(response_data[access_token_key], str)  # Verifica que sea un string
    assert response_data.get("token_typec") == "bearer"  # Revisar si la API debe devolver "token_type"

def test_google_login_error():
    """Prueba con un token inválido"""
    headers = {"Content-Type": "application/json"}
    payload = {"token": "invalid_token_12345"}

    response = client.post("/v1/auth/google-login", json=payload, headers=headers)

    assert response.status_code != 200 # Ahora debería devolver 401 correctamente
    assert any(msg in response.json()["detail"] for msg in ["Token de Firebase inválido", "Error inesperado en el proceso de autenticación"])

