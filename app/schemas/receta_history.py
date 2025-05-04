from pydantic import BaseModel
from datetime import datetime

class RecetaHistorySchema(BaseModel):
    id: int
    user_id: int
    transcript: str
    recipe: str
    created_at: datetime

    class Config:
        from_attributes  = True
