from pydantic import BaseModel
from typing import Optional

class ExerciseLogCreate(BaseModel):
    user_id: int
    exercise_id: int
    repetitions: int
    weight: Optional[float] = None
    completed: bool

class ExerciseLogUpdate(BaseModel):
    repetitions: Optional[int] = None
    weight: Optional[float] = None
    completed: Optional[bool] = None

class ExerciseLogResponse(BaseModel):
    id: int
    user_id: int
    exercise_id: int
    repetitions: int
    weight: Optional[float] = None
    completed: bool

    class Config:
        from_attributes = True  # Para compatibilidad con SQLAlchemy
