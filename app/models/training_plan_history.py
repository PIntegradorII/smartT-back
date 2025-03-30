from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP, func
from app.db.database import Base

class TrainingPlanHistory(Base):
    __tablename__ = "training_plans_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    training_plan_id = Column(Integer, ForeignKey("training_plans.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    lunes = Column(Text, nullable=True)
    martes = Column(Text, nullable=True)
    miercoles = Column(Text, nullable=True)
    jueves = Column(Text, nullable=True)
    viernes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now())
    archived_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())  # Campo que se usa en la consulta
    estado = Column(Integer, default=1)  # 1: Activo, 0: Inactivo
