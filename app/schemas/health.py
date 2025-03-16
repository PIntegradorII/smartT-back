from pydantic import BaseModel
from typing import Optional

class HealthDataBase(BaseModel):
    user_id: int
    tiene_condiciones: bool
    detalles_condiciones: Optional[str] = None
    lesiones: bool
    detalles_lesiones: Optional[str] = None
    confirmacion: bool

class HealthDataCreate(HealthDataBase):
    pass

class HealthDataUpdate(BaseModel):
    tiene_condiciones: Optional[bool] = None
    detalles_condiciones: Optional[str] = None
    lesiones: Optional[bool] = None
    detalles_lesiones: Optional[str] = None
    confirmacion: Optional[bool] = None

class HealthDataResponse(HealthDataBase):
    id: int

    class Config:
        orm_mode = True
