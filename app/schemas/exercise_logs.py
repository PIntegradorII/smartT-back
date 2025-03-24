from pydantic import BaseModel, Field
from typing import  Optional
from datetime import date


class ExerciseLogCreate(BaseModel):
    user_id: int
    date: date  # Cambiar log_date a date para coincidir con el modelo SQLAlchemy
    completed: bool

class ExerciseLogUpdate(BaseModel):
    date: Optional[date] = None
    completed: Optional[bool] = None

class ExerciseLogResponse(BaseModel):
    id: int
    user_id: int
    date: date
    completed: bool

    class Config:
        from_attributes = True



class ExerciseLogRequest(BaseModel):
    google_id: str

class ExerciseLogResponseLog(BaseModel):
    id: int
    user_id: int
    date: date
    completed: bool

    class Config:
        from_attributes = True  # Habilita conversión de SQLAlchemy a Pydantic
