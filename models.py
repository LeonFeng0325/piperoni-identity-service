from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# Database model defined here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False) # User email has to be unique
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False) # Hashed using SHA 256 and user specific info
    is_active = Column(Boolean, default=True) 
    source_service = Column(String) # the name of the service users is trying to login from