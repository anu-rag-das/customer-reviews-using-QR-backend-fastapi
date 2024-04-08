from app.config.db import SessionLocal
from sqlalchemy.orm import Session
from app.config.models import Users
from app.config.schemas import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session, user: User):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = Users(name = user.name, email=user.email, password=fake_hashed_password)
    print('creating a user', db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()