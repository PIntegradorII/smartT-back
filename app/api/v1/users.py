# Endpoints para usuarios

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
router = APIRouter()

@router.get('/users')
def get_users():
    return {"users": []}

@router.get('/users/{user_id}')
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user