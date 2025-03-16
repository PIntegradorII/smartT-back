# Endpoints de ejercicios
from fastapi import APIRouter
router = APIRouter()

@router.get('/exercises')
def get_exercises():
    return {"exercises": []}
