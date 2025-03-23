from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class ExerciseLogCreate(BaseModel):
    id: int
    user_id: int
    log_date: date
    completed: bool

class ExerciseLogUpdate(BaseModel):
    user_id: Optional[float] = None
    log_date: Optional[date] = None
    completed: Optional[bool] = None

class ExerciseLogResponse(BaseModel):
    id: int
    user_id: int
    log_date: date = Field(..., alias="date") 
    completed: bool

    class Config:
        from_attributes = True  # Para que SQLAlchemy lo mapee correctamente

class ExerciseLogRequest(BaseModel):
    google_id: str

class ExerciseLogResponseLog(BaseModel):
    id: int
    user_id: int
    date: date
    completed: bool

    class Config:
        from_attributes = True  # Habilita conversión de SQLAlchemy a Pydantic