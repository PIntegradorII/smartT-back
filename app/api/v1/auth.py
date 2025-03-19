# auth.py
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.schemas.user import UserResponse
import firebase_admin
from app.services.token_service import get_token_by_value
from firebase_admin import credentials, auth
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.core.config import settings
import jwt
import datetime
from app.services.token_service import delete_token, save_token  # Usamos el servicio de token
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
        
        # Obtener o crear usuario
        user = create_or_get_user(db, payload)

        # Obtener la ruta del usuario desde la base de datos
        ruta = db.execute(
            "SELECT COUNT(u.id) as ruta FROM personal_data pd "
            "INNER JOIN users u ON pd.user_id = u.id WHERE u.google_id = :google_id",
            {"google_id": google_id}
        ).scalar()  # `scalar()` obtiene un solo valor

        # Generación de JWT
        jwt_payload = {
            "sub": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        jwt_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        # Guardar token en la base de datos
        save_token(db, user.id, jwt_token)
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "ruta": ruta  # Agregamos la ruta en la respuesta
        }
    
    except Exception as e:
        logger.error(f"ERROR INESPERADO EN EL PROCESO DE AUTENTICACIÓN: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error inesperado en el proceso de autenticación")

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_obj = get_token_by_value(db, token)
    if not token_obj:
        raise HTTPException(status_code=400, detail="Token inválido o ya expirado")
    delete_token(db, token)
    return {"message": "Sesión cerrada correctamente"}