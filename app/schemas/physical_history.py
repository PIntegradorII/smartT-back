from pydantic import BaseModel
from datetime import datetime

class PhysicalHistorySchema(BaseModel):
    physical_id: int
    peso: float
    altura: float
    imc: float
    cintura: float
    pecho: float
    brazos: float
    piernas: float
    objetivo: str
    created_at: datetime
    archived_at: datetime
    estado: int

    class Config:
        orm_mode = True
