from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from app.config.db import SessionLocal
from sqlalchemy.orm import Session
from app.config.enums import RoleType
from app.config.models import Businesses, Reviews, Roles, Users
from app.config.schemas import Business, ReviewSchema, TokenData, User
from passlib.context import CryptContext
from jose import JWTError, jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session, user: User):
    hashed_password = get_password_hash(password = user.password)
    db_user = Users(username= user.username, name = user.name, email = user.email, gender = user.gender, password = hashed_password)
    role = db.query(Roles).filter(Roles.id == RoleType.ADMIN.value).first()
    db_user.roles.append(role)
    print('creating a user', db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_details(db: Session, current_user: User, data: dict):
    for key, value in data.items():
        if value is not None:
            setattr(current_user, key, value)
    try:
        db.add(current_user)
    except:
        db.add(db.merge(current_user))
    db.commit()
    return current_user

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    return db.query(Users).filter(Users.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get("JWT_SECRET_KEY"), algorithm=os.environ.get("JWT_ALGORITHM"))
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms=[os.environ.get("JWT_ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(next(get_db()), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_business(business: Business, user: User, db: Session):
    latitude, longitude = map(float, business.location.split(','))
    new_business = Businesses(
        name=business.name,
        description=business.description,
        latitude=latitude, 
        longitude=longitude,
        website=business.website
    )

    user = db.merge(user)
    user.businesses.append(new_business)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return business


def send_ok_response(response, message):
    return {
        "data":response,
        "success":True,
        "status_code": 200,
        "message":message
    }

def store_review(review: ReviewSchema, db : Session):
    business = db.query(Businesses).get(review.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found.")
    
    business.reviews.append(
        Reviews(
        cleanliness = review.cleanliness,
        communication = review.communication,
        location = review.location,
        accuracy = review.accuracy,
        value_for_money = review.value_for_money,
        comments = review.comments
        )
    )

    db.add(business)
    db.commit()
    
    return {
        "status_code": 200,
        "status": "Success",
        "message": "Added review successfully"
    }
    
def update_business_details(db: Session, business_id: int, data: dict):
    business = db.query(Businesses).get(business_id)
    for key, value in data.items():
        if value is not None:
            if key == 'location':
                latitude, longitude = map(float, data.get(key).split(','))
                business.latitude = latitude
                business.longitude = longitude
            setattr(business, key, value)
    try:
        db.add(business)
    except:
        db.add(db.merge(business))
    db.commit()
    return business


def change_user_password(passwords : dict, current_user: User, db: Session):
    if not verify_password(plain_password=passwords.get('old_password'), hashed_password=current_user.password):
        raise HTTPException(status_code=400, detail="Old and new passwords do not match")
    current_user.password = get_password_hash(password=passwords.get('new_password'))
    try:
        db.add(current_user)
    except:
        db.add(db.merge(current_user))
    db.commit()
    return current_user