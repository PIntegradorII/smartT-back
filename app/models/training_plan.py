from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import json

class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    lunes = Column(Text, nullable=True)
    martes = Column(Text, nullable=True)
    miercoles = Column(Text, nullable=True)
    jueves = Column(Text, nullable=True)
    viernes = Column(Text, nullable=True)

    def __init__(self, user_id, plan):
        """Inicializa un plan de entrenamiento, guardando cada día como JSON en formato string"""
        self.user_id = user_id
        self.lunes = json.dumps(plan.get("lunes", {}))  # Convierte el JSON a string
        self.martes = json.dumps(plan.get("martes", {}))
        self.miercoles = json.dumps(plan.get("miercoles", {}))
        self.jueves = json.dumps(plan.get("jueves", {}))
        self.viernes = json.dumps(plan.get("viernes", {}))
