from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config.db import SessionLocal
from sqlalchemy.orm import Session
from app.config.enums import RoleType
from app.config.models import Roles, Users
from app.config.schemas import TokenData, User
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
