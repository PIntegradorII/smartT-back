from app.models.token import Token
from sqlalchemy.orm import Session
import datetime

def save_token(db: Session, user_id: int, token: str, expires_at: datetime.datetime = None):
    new_token = Token(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token
