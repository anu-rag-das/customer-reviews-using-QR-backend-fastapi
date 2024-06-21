import re
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, constr, field_validator
from app.config.enums import GenderType

class User(BaseModel):
    username:constr(min_length=5)
    name:str
    gender:int
    email:EmailStr
    password:str

    @field_validator("username")
    def validate_name(cls, value):
        if not re.match(r"^[a-zA-Z0-9]+$", value.strip()):
            raise HTTPException(status_code=400,detail="username can only contain alphabets and digits without any space.")
        return value

    @field_validator("gender")
    def validate_gender(cls, value):
        if value not in [gender.value for gender in GenderType]:
            raise HTTPException(status_code=400,detail="Invalid gender.")
        return value
    
    @field_validator("password")
    def validate_password_strength(cls, value):
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+}{'\":;?/><,.\\-]).{8,}$", value):
            raise HTTPException(status_code=400,detail='password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
        return value

class UserUpdate(BaseModel):
    username:constr(min_length=5) = None
    name:str = None
    gender:int = None

    @field_validator("username")
    def validate_name(cls, value):
        if not re.match(r"^[a-zA-Z0-9]+$", value.strip()):
            raise HTTPException(status_code=400,detail="username can only contain alphabets and digits without any space.")
        return value

    @field_validator("gender")
    def validate_gender(cls, value):
        if value not in [gender.value for gender in GenderType]:
            raise HTTPException(status_code=400,detail="Invalid gender.")
        return value
    

class Business(BaseModel):
    name: str
    location: str
    description: str
    website: str = None
    
    @field_validator('location')
    def validate_location_format(cls, value):
        if not re.match(r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?$", value):
            raise ValueError('Invalid location format. It should be in the form of "latitude,longitude".')
        return value
    

class LoginSchema(BaseModel):
    login: str 
    password:str

    @field_validator("login")
    def validate_login(cls, value):
        if "@" in value:
            if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', value.strip()):
                raise HTTPException(status_code=401,detail="Invalid credentials.")
        else:
            if not re.match(r"^[a-zA-Z0-9]+$", value.strip()):
                raise HTTPException(status_code=401,detail="Invalid credentials.")
        return value
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserOut(BaseModel):
    username:str
    name:str
    gender:int
    email:EmailStr


class ReviewSchema(BaseModel):
    email : EmailStr
    business_id : int
    cleanliness : float
    communication : float
    location : float
    accuracy : float
    value_for_money : bool
    comments : str
    location: str

    @field_validator('location')
    def validate_location_format(cls, value):
        if not re.match(r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?$", value):
            raise ValueError('Invalid location format. It should be in the form of "latitude,longitude".')
        return value