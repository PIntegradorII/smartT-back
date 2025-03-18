from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.health import HealthData
from app.schemas.health import HealthDataCreate, HealthDataUpdate, HealthDataResponse

router = APIRouter()

#Obtener todos los historiales médicos
@router.get('/', response_model=list[HealthDataResponse])
def get_health_data(db: Session = Depends(get_db)):
    health_data = db.query(HealthData).all()
    return health_data

# Obtener un historial médico específico por ID
@router.get('/{health_id}', response_model=HealthDataResponse)
def get_health_by_id(health_id: int, db: Session = Depends(get_db)):
    health = db.query(HealthData).filter(HealthData.id == health_id).first()
    if not health:
        raise HTTPException(status_code=404, detail="Health data not found")
    return health

# Crear un nuevo historial médico
@router.post('/', response_model=HealthDataResponse)
def create_health_data(data: HealthDataCreate, db: Session = Depends(get_db)):
    new_health_data = HealthData(**data.dict())
    db.add(new_health_data)
    db.commit()
    db.refresh(new_health_data)
    return new_health_data

# Actualizar un historial médico existente
@router.put('/update/{health_id}', response_model=HealthDataResponse)
def update_health_data(health_id: int, data: HealthDataUpdate, db: Session = Depends(get_db)):
    health = db.query(HealthData).filter(HealthData.id == health_id).first()
    if not health:
        raise HTTPException(status_code=404, detail="Health data not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(health, key, value)
    db.commit()
    db.refresh(health)
    return health

# Eliminar un historial médico
@router.delete('/delete/{health_id}')
def delete_health_data(health_id: int, db: Session = Depends(get_db)):
    health = db.query(HealthData).filter(HealthData.id == health_id).first()
    if not health:
        raise HTTPException(status_code=404, detail="Health data not found")
    db.delete(health)
    db.commit()
    return {"message": "Health data deleted successfully"}

