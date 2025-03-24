from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.physical import PhysicalData
from app.schemas.physical import PhysicalDataCreate, PhysicalDataResponse

router = APIRouter()

# Crear un nuevo registro en physical_data
@router.post("/add", response_model=PhysicalDataResponse)
def create_physical_data(data: PhysicalDataCreate, db: Session = Depends(get_db)):
    new_data = PhysicalData(**data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

# Obtener un registro por ID
@router.get("/physical_data/{id}", response_model=PhysicalDataResponse)
def get_physical_data(id: int, db: Session = Depends(get_db)):
    physical_data = db.query(PhysicalData).filter(PhysicalData.id == id).first()
    if not physical_data:
        raise HTTPException(status_code=404, detail="Physical data not found")
    return physical_data

# Obtener todos los registros
@router.get("/", response_model=list[PhysicalDataResponse])
def get_all_physical_data(db: Session = Depends(get_db)):
    return db.query(PhysicalData).all()

# Actualizar un registro por ID
@router.put("/update/{id}", response_model=PhysicalDataResponse)
def update_physical_data(id: int, data: PhysicalDataCreate, db: Session = Depends(get_db)):
    physical_data = db.query(PhysicalData).filter(PhysicalData.id == id).first()
    if not physical_data:
        raise HTTPException(status_code=404, detail="Physical data not found")
    for key, value in data.dict().items():
        setattr(physical_data, key, value)
    db.commit()
    db.refresh(physical_data)
    return physical_data

# Eliminar un registro por ID
@router.delete("/delete/{id}")
def delete_physical_data(id: int, db: Session = Depends(get_db)):
    physical_data = db.query(PhysicalData).filter(PhysicalData.id == id).first()
    if not physical_data:
        raise HTTPException(status_code=404, detail="Physical data not found")
    db.delete(physical_data)
    db.commit()
    return {"detail": "Physical data deleted successfully"}

# Obtener por user_id
@router.get("/physical_data/user/{user_id}", response_model=PhysicalDataResponse)
def get_physical_data_by_user_id(user_id: int, db: Session = Depends(get_db)):
    physical_data = db.query(PhysicalData).filter(PhysicalData.user_id == user_id).first()
    if not physical_data:
        raise HTTPException(status_code=404, detail="Datos físicos no encontrados")
    return physical_data
