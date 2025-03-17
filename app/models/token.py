from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.user import User  # Import the User class
import datetime

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    expires_at = Column(TIMESTAMP, nullable=True)

    user = relationship("User", back_populates="tokens")

User.tokens = relationship("Token", back_populates="user")
