# Endpoints de rutinas fitness
from fastapi import APIRouter
router = APIRouter()

@router.get('/routines')
def get_routines():
    return {"routines": []}
