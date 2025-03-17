import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

firebase_cred_path = os.getenv("FIREBASE_ADMIN_SDK_JSON_PATH")

if firebase_cred_path is None:
    raise ValueError("La ruta del archivo de credenciales de Firebase no está definida en las variables de entorno.")

cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(cred)

def verify_google_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
