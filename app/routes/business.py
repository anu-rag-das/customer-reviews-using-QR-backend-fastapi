from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.config.enums import RoleType
from app.config.schemas import Business, User, ReviewSchema
from app.utils.helpers import get_current_user, get_db, create_business, get_user_by_email, send_ok_response, store_review
from sqlalchemy.orm import Session

business = APIRouter(tags=["business"])

@business.post("/business/", response_model=Business)
def add_business(business: Business,current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return create_business(business=business, user = current_user, db=db)

@business.get("/business/")
def get_business_of_current_user(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    response = [
        {
            "id": business.id,
            "name": business.name,
            "description": business.description,
            "website" : business.website
        }
        for business in current_user.businesses
    ]
    
    return send_ok_response(response = response, message = "Successfully fetched businesses." )

@business.post("/business/review/")
def add_review(review: ReviewSchema, db: Session = Depends(get_db)):
    if get_user_by_email(db=db, email=review.email):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )
    return store_review(review = review, db = db)