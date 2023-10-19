from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# Database models defined here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False) # User email has to be unique, and this is also user's username
    hashed_password = Column(String, nullable=False) # Hashed using SHA 256 and user specific info
    is_admin = Column(Boolean, default=False) # If user has the admin status, so far unused