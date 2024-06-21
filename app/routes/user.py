from typing import Annotated
from fastapi import APIRouter
from app.config.schemas import User, UserOut, UserUpdate
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.helpers import get_current_user, get_db, get_user, get_user_by_email, create_user, send_ok_response, update_user_details
from fastapi.encoders import jsonable_encoder


user = APIRouter(tags=["user"])

@user.post("/users/")
def add_user(user: User, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    elif get_user(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username is already taken")
    response = create_user(db=db, user=user)
    return send_ok_response(response=response, message="User created successfully")

@user.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return send_ok_response(response = current_user, message= "Fetched current user")

@user.put("/users/update/")
async def update_user(user: UserUpdate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    response = update_user_details(db=db, current_user=current_user, data=jsonable_encoder(user))
    return send_ok_response(response=response, message="User updated successfully")
    