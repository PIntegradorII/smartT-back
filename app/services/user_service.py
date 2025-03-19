from fastapi import Depends, HTTPException
import jwt
from sqlalchemy.orm import Session
from app.core.config import Settings
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_or_get_user(db: Session, user_info):
    user = db.query(User).filter(User.google_id == user_info["sub"]).first()

    if not user:
        user = User(
            google_id=user_info["sub"],
            email=user_info["email"],
            name=user_info["name"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(SessionLocal)):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")