from pydantic import BaseModel

class UserCreate(BaseModel):
    google_id: str
    email: str
    name: str
    avatar: str

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True
