from pydantic import BaseModel
from typing import Optional

class DietPlanBase(BaseModel):
    user_id: int
    transcript: Optional[str] = None
    plan: Optional[str] = None

class DietPlanCreate(DietPlanBase):
    pass

class DietPlanUpdate(BaseModel):
    transcript: Optional[str] = None
    plan: Optional[str] = None

class DietPlanResponse(DietPlanBase):
    id: int

    class Config:
        orm_mode = True  # Esto es necesario para que Pydantic pueda trabajar con ORM (como SQLAlchemy)
