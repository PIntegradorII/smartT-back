from app.models.physical_history import PhysicalHistory
from app.models.physical import PhysicalData
from app.schemas.physical_history import PhysicalHistorySchema
from sqlalchemy.orm import Session

def get_physical_history_by_user(db: Session, user_id: int):
    result = db.query(PhysicalHistory).join(PhysicalData).filter(PhysicalData.user_id == user_id).all()
    return result

def create_physical_history(db: Session, physical_data: PhysicalHistorySchema):
    """
    Crea un nuevo registro en el historial de medidas físicas basado en physical_id.
    """
    # Crear el objeto PhysicalHistory a partir de los datos recibidos
    new_physical_history = PhysicalHistory(
        physical_id=physical_data.physical_id,  # Aquí usamos physical_id en lugar de user_id
        peso=physical_data.peso,
        altura=physical_data.altura,
        cintura=physical_data.cintura,
        pecho=physical_data.pecho,
        brazos=physical_data.brazos,
        piernas=physical_data.piernas,
        imc=physical_data.imc,
        objetivo=physical_data.objetivo,
    )

    # Agregar a la sesión y guardar en la base de datos
    db.add(new_physical_history)
    db.commit()
    db.refresh(new_physical_history)  # Refresca el objeto para obtener el ID generado

    return new_physical_history