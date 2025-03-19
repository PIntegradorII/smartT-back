# auth_service.py

from sqlalchemy.orm import Session
from app.models.user import User
from google.auth.transport import requests
from google.oauth2 import id_token
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def authenticate_google_user(token: str, db: Session):
    """ Verifica el token de Google y maneja la creación de usuario """
    try:
        logger.debug(f"Verificando token de Google: {token}")
        payload = id_token.verify_oauth2_token(
            token, requests.Request(), settings.FIREBASE_PROJECT_ID
        )
        logger.debug(f"Payload verificado: {payload}")

        google_id = payload["sub"]
        email = payload["email"]
        name = payload.get("name", "")
        avatar = payload.get("picture", "")

        user = db.query(User).filter(User.google_id == google_id).first()

        if not user:
            logger.debug(f"Usuario no encontrado, creando nuevo usuario: {email}")
            user = User(
                google_id=google_id, 
                email=email, 
                name=name, 
                avatar=avatar
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.debug(f"Nuevo usuario creado: {user.id}")

        return user

    except Exception as error:
        logger.error(f"Error en la autenticación de Google: {error}")
        raise
