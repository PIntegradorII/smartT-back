# Modelo de usuario
from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    health_data = relationship("HealthData", back_populates="user", cascade="all, delete-orphan")
