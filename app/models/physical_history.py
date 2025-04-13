from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class PhysicalHistory(Base):
    __tablename__ = "physical_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    physical_id = Column(Integer, ForeignKey("physical_data.id"), nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)
    cintura = Column(Float, nullable=False)
    pecho = Column(Float, nullable=False)
    brazos = Column(Float, nullable=False)
    piernas = Column(Float, nullable=False)
    objetivo = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    archived_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())  # Campo que se usa en la consulta
    estado = Column(Integer, default=1)  # 1: Activo, 0: Inactivo
