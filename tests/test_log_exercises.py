import pytest
import httpx

BASE_URL = "https://smartt-back.onrender.com/v1/log_exercises/exercise/weekly/"

@pytest.mark.parametrize(
    "google_id, expected_status, expected_response",
    [
        # ✅ Caso exitoso: Usuario 1
        (
            "Y8q3uaCzIJafXWJvMin5GifaM8A2",
            200,
            [
                {
                    "day": "Lunes",
                    "completed": False,
                    "date": "24 de March"
                }
            ],
        ),
        # ✅ Caso exitoso: Usuario 2
        (
            "2yTin9cdtDfpalkxwk1HPg1MRCO2",
            200,
            [
                {
                    "day": "Lunes",
                    "completed": False,
                    "date": "24 de March"
                }
            ],
        ),
        # ✅ Caso exitoso: Usuario 3
        (
            "ztQQgJuyRWbgNUNUE7p9k0SUUb33",
            200,
            [
                {
                    "day": "Lunes",
                    "completed": False,
                    "date": "24 de March"
                }
            ],
        ),
        # ❌ Caso fallido: Google ID incorrecto
        (
            "INVALID_GOOGLE_ID",
            404,
            {"detail": "No se encontraron registros para este usuario"},
        ),
       # ❌ Caso fallido: Google ID incorrecto
        (
            "INVALID_GOOGLE_ID",
            404,
            {"detail": "No se encontraron registros para este usuario"},
        ),
    ],
)
def test_log_exercise_weekly(google_id, expected_status, expected_response):
    """Prueba el endpoint que obtiene el log semanal de ejercicios con diferentes Google IDs"""
    payload = {"google_id": google_id}

    response = httpx.post(BASE_URL, json=payload)

    assert response.status_code == expected_status
    assert response.json() == expected_response
