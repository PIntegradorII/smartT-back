from pydantic import BaseModel
import datetime

class TokenCreate(BaseModel):
    user_id: int
    token: str
    expires_at: datetime.datetime

class TokenResponse(TokenCreate):
    id: int

    class Config:
        from_attributes  = True
