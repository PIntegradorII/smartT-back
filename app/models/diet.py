from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.db.database import Base
from sqlalchemy.orm import relationship

class DietPlan(Base):
    __tablename__ = "diet_plan"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transcript = Column(Text, nullable=True)
    plan = Column(Text, nullable=True)

    # Relación con el modelo User
    user = relationship("User", back_populates="diet_plan")

