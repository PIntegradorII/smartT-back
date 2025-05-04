from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.receta import RecetaHistorico
from app.models.user import User  # Importar el modelo de Usuario
from app.db.database import get_db
from app.schemas.receta_history import RecetaHistorySchema
from app.services.receta_history import get_receta_plan_history    # Asegúrate de que el servicio esté importado

router = APIRouter()

@router.get("/history/{google_id}", response_model=List[RecetaHistorySchema])
def get_receta_history(google_id: str, db: Session = Depends(get_db)):
    """
    Obtiene el historial de rutinas de un usuario basado en su Google ID.
    """
    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return get_receta_plan_history(db, user.id)  # Se usa el ID real del usuario