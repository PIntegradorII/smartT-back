import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.core.config import settings
import jwt
import datetime
from app.services.token_service import save_token  # Usamos el servicio de token
from app.services.user_service import create_or_get_user  # Usamos el servicio de usuario
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Cargar las credenciales del archivo de servicio de Firebase desde la variable de entorno
firebase_cred_path = os.getenv("FIREBASE_ADMIN_SDK_JSON_PATH", "./firebase-adminsdk.json")
cred = credentials.Certificate(firebase_cred_path)

# Inicializar la aplicación de Firebase Admin
firebase_admin.initialize_app(cred)

# Configuración del logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

router = APIRouter()

# Esquema para el request body
class GoogleLoginRequest(BaseModel):
    token: str

# Obtener conexión a la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Verificar token de Firebase
def verify_firebase_token(token: str):
    try:
        # Verificar el token de Firebase con el argumento correcto
        decoded_token = auth.verify_id_token(token, clock_skew_seconds=60)
        return decoded_token
    except auth.InvalidIdTokenError as e:
        raise HTTPException(status_code=400, detail=f"Token de Firebase inválido: {e}")


@router.post("/google-login")
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        token = request.token
        # Verificación del token con Firebase Admin SDK
        payload = verify_firebase_token(token)
        google_id = payload["sub"]
        email = payload["email"]
        name = payload.get("name", "")
        avatar = payload.get("picture", "")
        
        # Usamos el servicio de usuario para crear o obtener un usuario
        user = create_or_get_user(db, payload)

        # Generación de JWT
        jwt_payload = {
            "sub": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        }
        jwt_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm="HS256")
        
        # Usamos el servicio de token para guardar el token
        save_token(db, user.id, jwt_token)
        
        return {"access_token": jwt_token, "token_type": "bearer"}
    
    except Exception as e:
        logger.error(f"ERROR INESPERADO EN EL PROCESO DE AUTENTICACIÓN: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error inesperado en el proceso de autenticación")
