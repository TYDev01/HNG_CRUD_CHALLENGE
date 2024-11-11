# from .database import Base
# from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field
from typing import Optional


class RegisterUser(SQLModel, table=True):
    __tablename__ = "registeruser"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: Optional[str] = Field(index=True, unique=True)
    password: str