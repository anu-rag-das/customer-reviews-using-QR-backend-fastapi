from datetime import datetime
from xmlrpc.client import Boolean
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Integer
from app.config.db import Base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

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
    businesses = relationship("Businesses", secondary="business_user", back_populates="users")

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
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    website = Column(String(255))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    #relationships
    users = relationship("Users",secondary="business_user", back_populates="businesses")

class BusinessUser(Base):
    __tablename__ = "business_user"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id"), primary_key=True)