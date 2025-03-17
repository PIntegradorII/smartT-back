import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

# Cargar las credenciales de Firebase
firebase_cred_path = os.getenv("FIREBASE_ADMIN_SDK_JSON_PATH")

if not firebase_cred_path:
    raise ValueError("La ruta del archivo de credenciales de Firebase no está definida.")

cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(cred)

# Función para verificar el token de Firebase
def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
