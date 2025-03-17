# Modelo de usuario
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from app.db.database import Base
from sqlalchemy.orm import relationship

class HealthData(Base):
    __tablename__ = "health_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tiene_condiciones = Column(Boolean, nullable=False)
    detalles_condiciones = Column(Text, nullable=True)
    lesiones = Column(Boolean, nullable=False)
    detalles_lesiones = Column(Text, nullable=True)
    confirmacion = Column(Boolean, nullable=False)

    # Relación opcional
    user = relationship("User", back_populates="health_data")
from app.models.user import User