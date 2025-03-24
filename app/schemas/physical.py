from pydantic import BaseModel, Field
from typing import Optional


# Esquema para crear datos físicos
class PhysicalDataCreate(BaseModel):
    user_id: int
    peso: float
    altura: float
    imc: float
    cintura: float
    pecho: float
    brazos: float
    piernas: float
    objetivo: str


# Esquema para retornar datos físicos (respuesta del backend)
class PhysicalDataResponse(PhysicalDataCreate):
    id: int

    class Config:
        orm_mode = True
