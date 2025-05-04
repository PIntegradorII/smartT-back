from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class ImgMaquinaSchema(BaseModel):
    id: int
    user_id: int
    maquina_data: str
    image_path: str
    created_at: datetime

    class Config:
        model_config  = True
