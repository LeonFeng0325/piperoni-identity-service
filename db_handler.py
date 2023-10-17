from auth import get_password_hash
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import delete
from database import get_db
from models import User as user_table
from schemas import User




# DB Handler class that handles all database interaction
class DBHandler:
    ## Constructor
    def __init__(self, db: Session) -> None:
        super().__init__()
        self._db = db
    
    def get_user_by_full_name(self, first_name: str, last_name: str):
        return self._db.query(user_table).filter(user_table.first_name == first_name, user_table.last_name == last_name).all()
    
    def get_user_by_email(self, email: str):
        return self._db.query(user_table).filter(user_table.email == email).first()
    
    def get_user_by_hashed_password(self, hash: str):
        return self._db.query(user_table).filter(user_table.hashed_password == hash).first()
    
    def get_users(self, skip: int = 0, limit: int = 100):
        return self._db.query(user_table).offset(skip).limit(limit).all()
    
    def create_user(self, user: User):
        hash_password = get_password_hash(user.email)
        db_user = user_table(**user.model_dump(), hashed_password=hash_password)
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)

        return db_user
    
    def delete_user_by_hash(self, hash: str):
        query = delete(user_table).where(user_table.hashed_password == hash)
        response = self._db.execute(query)

        return response
    
    def delete_user_by_email(self, email: str):
        query = delete(user_table).where(user_table.email == email)
        response = self._db.execute(query)

        return response

def get_db_handler(db=Depends(get_db)):
    return DBHandler(db)
