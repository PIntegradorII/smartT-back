from pydantic import BaseModel
from typing import Optional

class HealthDataBase(BaseModel):
    user_id: int
    tiene_condiciones: str
    detalles_condiciones: Optional[str] = None
    lesiones: Optional[str] = None  # Ahora puede ser None
    confirmacion: str

class HealthDataCreate(HealthDataBase):
    pass

class HealthDataUpdate(BaseModel):
    tiene_condiciones: Optional[str] = None
    detalles_condiciones: Optional[str] = None
    lesiones: Optional[str] = None
    confirmacion: Optional[str] = None

class HealthDataResponse(HealthDataBase):
    id: int

    class Config:
        from_attributes  = True
