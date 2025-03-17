from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    avatar = Column(String, nullable=True)
    created_at = Column(Integer, default=0)

User.tokens = relationship("Token", back_populates="user")
