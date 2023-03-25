from sqlalchemy import Column, String, Boolean, Integer
from .database import Base

class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    api_key = Column(String, nullable=False)