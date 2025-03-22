# Endpoints para usuarios

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
router = APIRouter()

@router.get('/users')
def get_users():
    return {"users": []}
