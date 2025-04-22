from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.physical import PhysicalData
from app.models.user import User  # Importar el modelo de Usuario
from app.db.database import get_db
from app.schemas.physical_history import PhysicalHistorySchema
from app.services.physical_history import get_physical_history_by_user, create_physical_history    # Asegúrate de que el servicio esté importado

router = APIRouter()

@router.get("/physical_history/{google_id}", response_model=List[PhysicalHistorySchema])
def read_physical_history(google_id: str, db: Session = Depends(get_db)):
    """
    Obtiene el historial de medidas físicas de un usuario basado en su Google ID.
    """
    # Buscar el usuario por su Google ID
    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Usar el `user_id` para obtener el historial de medidas físicas
    return get_physical_history_by_user(db, user.id)


@router.post("/physical_history", response_model=PhysicalHistorySchema)
def create_physical_history_record(
    physical_data: PhysicalHistorySchema, db: Session = Depends(get_db)
):
    """
    Crea un nuevo registro en el historial de medidas físicas de un usuario.
    """
    # Buscar el PhysicalData por su ID
    physical_data_record = db.query(PhysicalData).filter(PhysicalData.id == physical_data.physical_id).first()
    if not physical_data_record:
        raise HTTPException(status_code=404, detail="Datos físicos no encontrados")

    # Llamar al servicio para crear el registro de historial físico
    try:
        new_physical_history = create_physical_history(db, physical_data)
        return new_physical_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el historial físico: {str(e)}")
