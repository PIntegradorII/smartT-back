from pydantic import BaseModel
from typing import Optional, Dict, Any

class TrainingPlanCreate(BaseModel):
    user_id: int
    lunes: Optional[Dict[str, Any]] = None
    martes: Optional[Dict[str, Any]] = None
    miercoles: Optional[Dict[str, Any]] = None
    jueves: Optional[Dict[str, Any]] = None
    viernes: Optional[Dict[str, Any]] = None
