from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class ImgMaquina(Base):
    __tablename__ = 'img_maquinas'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    maquina_data = Column(Text, nullable=False)  # Guardamos el JSON con los datos de la máquina
    image_path = Column(String, nullable=False)  # Ruta de la imagen guardada
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="img_maquinas")