from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class PersonalData(Base):
    __tablename__ = "personal_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    genero = Column(String, nullable=False)

    user = relationship("User", back_populates="personal_data")
from app.models.user import User