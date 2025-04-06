from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func  # Importar func para usar la función `now()`
from app.db.database import Base

class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    transcript =  Column(JSON, nullable=False)
    recipe = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=func.now())  # Cambiar a DateTime
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Cambiar a DateTime

class RecetaHistorico(Base):
    __tablename__ = 'recetas_historico'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    transcript =  Column(JSON, nullable=False)
    recipe =  Column(JSON, nullable=False)
    created_at = Column(DateTime, default=func.now())  # Cambiar a DateTime
