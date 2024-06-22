from typing import Annotated
from fastapi import APIRouter, Depends
from app.config.schemas import Business, User, ReviewSchema, BusinessUpdate
from app.utils.helpers import get_current_user, get_db, create_business, send_ok_response, store_review, update_business_details
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

business = APIRouter(tags=["business"])

@business.post("/business/", response_model=Business)
def add_business(business: Business,current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return create_business(business=business, user = current_user, db=db)

@business.get("/business/")
def get_businesses(current_user: Annotated[User, Depends(get_current_user)]):
    response = [ 
                    {   
                        "business_id" : business.id, 
                        "name" : business.name, 
                        "description" : business.description, 
                        "website" : business.website, 
                        "reviews" : [
                                        { 
                                            "cleanliness" : review.cleanliness, 
                                            "communication": review.communication, 
                                            "location" : review.location, 
                                            "accuracy" : review.accuracy, 
                                            "value_for_money": review.value_for_money, 
                                            "comments": review.comments 
                                        } for review in business.reviews
                                    ] 
                    } for business in current_user.businesses   
                ]
    return send_ok_response(response=response, message="Successfully fetched businesses")


@business.post("/business/reviews/")
def add_review(review: ReviewSchema, db: Session = Depends(get_db)):
    return store_review(review = review, db = db)


@business.put("/business/{business_id}")
async def update_business(business_id: int, current_user: Annotated[User, Depends(get_current_user)], business: BusinessUpdate, db: Session = Depends(get_db)):
    response = update_business_details(db=db, business_id = business_id, data = jsonable_encoder(business))
    return send_ok_response(response=response, message="Business updated successfully")
