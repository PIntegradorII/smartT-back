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

    health_data = relationship("HealthData", back_populates="user", cascade="all, delete-orphan")
    personal_data = relationship("PersonalData", back_populates="user", cascade="all, delete-orphan")
    physical_data = relationship("PhysicalData", back_populates="user", cascade="all, delete-orphan")
    diet_plan = relationship("DietPlan", back_populates="user", cascade="all, delete-orphan")
    img_maquinas = relationship("ImgMaquina", back_populates="user")
User.tokens = relationship("Token", back_populates="user")
