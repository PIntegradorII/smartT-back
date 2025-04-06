import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000/v1/training/training-plan/google"

@pytest.mark.parametrize(
    "google_id, expected_status, expected_response",
    [
        # ✅ Caso exitoso
        (
            "Y8q3uaCzIJafXWJvMin5GifaM8A2",
            200,
            {
                "user_id": 9,
                "martes": {
                    "titulo": "Cardio y core",
                    "musculos": ["cardiovascular", "core"],
                    "ejercicios": [
                        {"ejercicio": "correr en bicicleta", "series": 1, "repeticiones": "20-30 minutos"},
                        {"ejercicio": "crunches", "series": 3, "repeticiones": "15-20"},
                        {"ejercicio": "elevaciones de piernas", "series": 3, "repeticiones": "15-20"},
                    ],
                },
                "jueves": {
                    "titulo": "Cardio y core",
                    "musculos": ["cardiovascular", "core"],
                    "ejercicios": [
                        {"ejercicio": "caminar en cinta", "series": 1, "repeticiones": "30-40 minutos"},
                        {"ejercicio": "rusas", "series": 3, "repeticiones": "15-20"},
                        {"ejercicio": "elevaciones laterales", "series": 3, "repeticiones": "15-20"},
                    ],
                },
                "lunes": {
                    "titulo": "Entrenamiento de cuerpo completo",
                    "musculos": ["piernas", "hombros", "core"],
                    "ejercicios": [
                        {
                            "ejercicio": "sentadillas",
                            "series": 4,
                            "repeticiones": "12-15",
                            "imagen": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/4-qQbFkbf3E6kGxk2YvHPXjGdwEi2EAe.svg",
                        },
                        {
                            "ejercicio": "flexiones de pecho",
                            "series": 3,
                            "repeticiones": "10-12",
                            "imagen": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/4-qQbFkbf3E6kGxk2YvHPXjGdwEi2EAe.svg",
                        },
                        {
                            "ejercicio": "planchas",
                            "series": 3,
                            "repeticiones": "30-60 segundos",
                            "imagen": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/4-qQbFkbf3E6kGxk2YvHPXjGdwEi2EAe.svg",
                        },
                    ],
                },
                "miercoles": {
                    "titulo": "Entrenamiento de hombros y brazos",
                    "musculos": ["hombros", "brazos"],
                    "ejercicios": [
                        {"ejercicio": "flexiones con apoyo", "series": 3, "repeticiones": "10-12"},
                        {"ejercicio": "prensa militar con mancuernas", "series": 3, "repeticiones": "10-12"},
                        {"ejercicio": "remo con mancuernas", "series": 3, "repeticiones": "10-12"},
                    ],
                },
                "id": 1,
                "viernes": {
                    "titulo": "Entrenamiento de piernas y glúteos",
                    "musculos": ["piernas", "gluteos"],
                    "ejercicios": [
                        {"ejercicio": "prensa de piernas", "series": 4, "repeticiones": "12-15"},
                        {"ejercicio": "lunges", "series": 3, "repeticiones": "10-12 por pierna"},
                        {"ejercicio": "puentes", "series": 3, "repeticiones": "15-20"},
                    ],
                },
            },
        ),
        # ❌ Caso fallido: Google ID inválido
        (
            "codigoMal",
            404,
            {"detail": "Usuario no encontrado"},
        ),
    ],
)
def test_get_training_plan(google_id, expected_status, expected_response):
    """Prueba el endpoint GET /v1/training/training-plan/google/{google_id}"""
    response = httpx.get(f"{BASE_URL}/{google_id}")

    assert response.status_code == expected_status
    assert response.json() == expected_response
