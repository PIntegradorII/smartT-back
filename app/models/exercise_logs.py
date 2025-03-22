from sqlalchemy import Boolean, Column, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base  # Asegurar que la importación es correcta
from app.models.user import User   # Importar User después de Base para evitar problemas de referencia circular

class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Agregar nullable=False para mayor integridad
    date = Column(Date, index=True, nullable=False)
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="exercise_logs")  # Relación corregida

# Definir la relación en User (asegurar que existe en el modelo User)
User.exercise_logs = relationship("ExerciseLog", back_populates="user", cascade="all, delete-orphan")
