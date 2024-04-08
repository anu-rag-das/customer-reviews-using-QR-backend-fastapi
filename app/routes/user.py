from fastapi import APIRouter
from app.config.schemas import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.helpers import get_db, get_user_by_email, create_user


user = APIRouter(tags=["user"])

@user.post("/users/", response_model=User)
def add_user(user: User, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
