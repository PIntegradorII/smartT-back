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
    
    # Convertir el string JSON a dict
    @property
    def nutrition_plan(self):
        try:
            return json.loads(self.plan) if self.plan else None
        except json.JSONDecodeError:
            return None

