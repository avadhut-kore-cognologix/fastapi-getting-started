from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    role = Column(String)
    email = Column(String)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)