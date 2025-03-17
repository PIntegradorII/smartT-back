from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def create_or_get_user(db: Session, user_info):
    user = db.query(User).filter(User.google_id == user_info["sub"]).first()

    if not user:
        user = User(
            google_id=user_info["sub"],
            email=user_info["email"],
            name=user_info["name"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
