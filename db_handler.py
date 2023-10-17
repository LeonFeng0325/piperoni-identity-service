from auth import get_password_hash
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import delete
from database import get_db
from models import User as user_table
from schemas import User
from exception import AlreadyExistsError, InvalidParameterError, NotFoundError


# DB Handler class that handles all database interactions
class DBHandler:

    def __init__(self, db: Session) -> None:
        super().__init__()
        self._db = db
    
    def get_user_by_full_name(self, first_name: str, last_name: str):
        return self._db.query(user_table).filter(user_table.first_name == first_name.lower().strip(), user_table.last_name == last_name.lower().strip()).all()
    
    def get_user_by_email(self, email: str):
        return self._db.query(user_table).filter(user_table.email == email.strip()).first()
    
    def get_user_by_hash(self, hash: str):
        return self._db.query(user_table).filter(user_table.hashed_password == hash.strip()).first()
    
    def get_users(self, skip: int = 0, limit: int = 100):
        return self._db.query(user_table).offset(skip).limit(limit).all()
    
    def create_user(self, user: User):
        user_email = user.email.strip()
        first_name = user.first_name.lower().strip()
        last_name = user.last_name.lower().strip()

        db_user = self.get_user_by_email(user_email)
        if db_user:
            raise AlreadyExistsError("Email already exists.")
        if not user_email or len(user_email) == 0:
            raise InvalidParameterError("Email is required.")
        if not first_name or len(first_name) == 0:
            raise InvalidParameterError("First name is required.")
        if not last_name or len(last_name) == 0:
            raise InvalidParameterError("Last name is required.")


        user_hash = get_password_hash(user_email) # Unique to each user
    
        db_user = user_table(email=user.email, is_active=user.is_active, first_name=first_name, last_name=last_name, hashed_password=user_hash)

        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)

        return db_user
    
    def delete_user_by_hash(self, hash: str):
        db_user = self.get_user_by_hash(hash)
        if not db_user:
            raise NotFoundError("User hash not found.")
        query = delete(user_table).where(user_table.hashed_password == hash.strip())
        response = self._db.execute(query)

        self._db.commit()

        return response
    
    def delete_user_by_email(self, email: str):
        db_user = self.get_user_by_email(email)
        if not db_user:
            raise NotFoundError("User email not found.")
        query = delete(user_table).where(user_table.email == email.strip())
        response = self._db.execute(query)

        self._db.commit()

        return response


def get_db_handler(db=Depends(get_db)):
    return DBHandler(db)
