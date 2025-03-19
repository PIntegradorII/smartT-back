from app.models.token import Token
from sqlalchemy.orm import Session
import datetime

def save_token(db: Session, user_id: int, token: str, expires_at=None):
    new_token = Token(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token

def delete_token(db: Session, token: str):
    db.query(Token).filter(Token.token == token).delete()
    db.commit()


def get_token_by_value(db: Session, token: str):
    return db.query(Token).filter(Token.token == token).first()