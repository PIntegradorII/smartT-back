from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.personal_data import PersonalData
from app.schemas.personal_data import PersonalDataCreate, PersonalDataResponse
from app.models.user import User

router = APIRouter()

# Crear un nuevo registro en personal_data
@router.post("/add", response_model=PersonalDataResponse)
def create_personal_data(data: PersonalDataCreate, db: Session = Depends(get_db)):
    new_data = PersonalData(**data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

# Obtener un registro por ID
@router.get("/personal_data/{id}", response_model=PersonalDataResponse)
def get_personal_data(id: int, db: Session = Depends(get_db)):
    personal_data = db.query(PersonalData).filter(PersonalData.id == id).first()
    if not personal_data:
        raise HTTPException(status_code=404, detail="Personal data not found")
    return personal_data

# Obtener todos los registros
@router.get("/", response_model=list[PersonalDataResponse])
def get_all_personal_data(db: Session = Depends(get_db)):
    return db.query(PersonalData).all()

# Actualizar un registro por ID
@router.put("/update/{user_id}", response_model=PersonalDataResponse)
def update_personal_data(user_id: int, data: PersonalDataCreate, db: Session = Depends(get_db)):
    # Buscar los datos personales usando user_id
    personal_data = db.query(PersonalData).filter(PersonalData.user_id == user_id).first()
    
    # Manejo de caso si no se encuentra el usuario
    if not personal_data:
        raise HTTPException(status_code=404, detail="Personal data not found")
    
    # Actualizar los campos de personal_data con los valores nuevos
    for key, value in data.dict().items():
        setattr(personal_data, key, value)
    
    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(personal_data)
    
    return personal_data


# Eliminar un registro por ID
@router.delete("/delete/{id}")
def delete_personal_data(id: int, db: Session = Depends(get_db)):
    personal_data = db.query(PersonalData).filter(PersonalData.id == id).first()
    if not personal_data:
        raise HTTPException(status_code=404, detail="Personal data not found")
    db.delete(personal_data)
    db.commit()
    return {"detail": "Personal data deleted successfully"}

@router.get('/personal_data/user/{user_id}')
def get_personal_data_by_user_id(user_id: int, db: Session = Depends(get_db)):
    personal_data = db.query(PersonalData).filter(PersonalData.user_id == user_id).first()
    if not personal_data:
        raise HTTPException(status_code=404, detail="Datos personales no encontrados")
    return personal_data
