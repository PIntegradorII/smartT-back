from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class PhysicalData(Base):
    __tablename__ = "physical_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)
    cintura = Column(Float, nullable=False)
    pecho = Column(Float, nullable=False)
    brazos = Column(Float, nullable=False)
    piernas = Column(Float, nullable=False)
    objetivo = Column(String, nullable=False)

    user = relationship("User", back_populates="physical_data")
