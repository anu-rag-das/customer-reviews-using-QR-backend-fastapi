from sqlalchemy import Column, String, Integer
from app.config.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False,unique=True, index=True)
    password = Column(String(255),nullable=False)