import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, get_db
from app.db.database import engine  # Ajusta la ruta según la estructura de tu proyecto

# Sobrescribir `get_db` para usar la misma base de datos
@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = next(get_db())
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



# Pruebas unitarias
def test_create_personal_data(client):
    payload = {
        "user_id": 44,
        "edad": 25,
        "genero": "M"
    }
    response = client.post("/v1/personal_data/add", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == payload["user_id"]
    assert data["edad"] == payload["edad"]
    assert data["genero"] == payload["genero"]



def test_create_exercise_log(client):
    payload = {
        "user_id": 44,
        "date": "2025-03-24",
        "completed": False
    }
    response = client.post("/v1/log_exercises/exercise/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == payload["user_id"]
    assert data["date"] == payload["date"]
    assert data["completed"] == payload["completed"]

def test_create_health_data(client):
    payload = {
        "user_id": 44,
        "tiene_condiciones": "Sí",
        "detalles_condiciones": "Diabetes tipo 2",
        "lesiones": "Fractura en el brazo",
        "confirmacion": "Confirmado"
    }

    # Llamada al endpoint
    response = client.post("/v1/health", json=payload)

    # Verificaciones
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == payload["user_id"]
    assert data["tiene_condiciones"] == payload["tiene_condiciones"]
    assert data["detalles_condiciones"] == payload["detalles_condiciones"]
    assert data["lesiones"] == payload["lesiones"]
    assert data["confirmacion"] == payload["confirmacion"]