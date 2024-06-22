from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Integer, Float, BOOLEAN
from app.config.db import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    gender = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False,unique=True, index=True)
    password = Column(String(255), nullable=False)
    #relationships
    roles = relationship("Roles", secondary="role_user", back_populates="users")
    businesses = relationship("Businesses", back_populates="users")

class RoleUser(Base):
    __tablename__ = "role_user"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    role_id = Column(BigInteger, ForeignKey("roles.id"), primary_key=True)

class Roles(Base):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    #relationship
    users = relationship("Users", secondary="role_user", back_populates="roles")

class Businesses(Base):
    __tablename__ = "businesses"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False) 
    website = Column(String(255))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    #relationships
    users = relationship("Users", back_populates="businesses")
    reviews = relationship("Reviews", back_populates="business")

class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id"), nullable=False)
    cleanliness = Column(Float, nullable=True)
    communication = Column(Float, nullable=True)
    location = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    value_for_money = Column(BOOLEAN, nullable=True)
    comments = Column(String(255))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    # Relationships
    business = relationship("Businesses", back_populates="reviews", uselist=False)
