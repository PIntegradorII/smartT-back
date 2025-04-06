from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TrainingPlanHistorySchema(BaseModel):
    id: int
    user_id: int
    lunes: Optional[str] = None
    martes: Optional[str] = None
    miercoles: Optional[str] = None
    jueves: Optional[str] = None
    viernes: Optional[str] = None
    created_at: datetime
    fecha_estado: Optional[datetime] = None  # Campo que unifica updated_at y archived_at
    estado: int  
    objetivo: Optional[str] = None

    class Config:
        orm_mode = True
