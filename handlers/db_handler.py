from auth.auth_password import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from models import User as user_table, Genre as genre_table, PersonalGenre as personal_genre_table
from schemas import User, Genre
from exception import AlreadyExistsError, InvalidParameterError, NotFoundError
from utils.email_verification import is_valid_email
from auth.auth_password import verify_password
from typing import List
from preflight import genre_list

# DB Handler class that handles all database interactions
class DBHandler:

    def __init__(self, db: Session) -> None:
        super().__init__()
        self._db = db
    
    # Users table queries
    def get_user_by_full_name(self, first_name: str, last_name: str):
        return self._db.query(user_table).filter(user_table.first_name == first_name.lower().strip(), user_table.last_name == last_name.lower().strip()).all()
    
    def get_user_by_email(self, email: str):
        return self._db.query(user_table).filter(user_table.email == email.strip()).first()
    
    def get_user_by_hash(self, hash: str):
        return self._db.query(user_table).filter(user_table.hashed_password == hash.strip()).first()
    
    def get_users(self, skip: int = 0, limit: int = 100):
        return self._db.query(user_table).offset(skip).limit(limit).all()
    
    def authenticate_user(self, email: str, password: str):
        db_user = self.get_user_by_email(email)
        if not db_user:
            return False
        if not verify_password(password ,db_user.hashed_password):
            return False
        return db_user
    
    def create_user(self, user: User):
        user_email = user.email.strip()
        password = user.password.strip()
        first_name = user.first_name.lower().strip()
        last_name = user.last_name.lower().strip()

        db_user = self.get_user_by_email(user_email)
        # Sanity check
        if db_user:
            raise AlreadyExistsError("Email already exists.")
        if not user_email or len(user_email) == 0:
            raise InvalidParameterError("Email is required.")
        if not is_valid_email(user_email):
            raise InvalidParameterError("Please provide a valid email.")
        if not first_name or len(first_name) == 0:
            raise InvalidParameterError("First name is required.")
        if not last_name or len(last_name) == 0:
            raise InvalidParameterError("Last name is required.")
        if not password or len(password) == 0:
            raise InvalidParameterError("Password is required")

        user_hash = get_password_hash(password) # Unique to each user
        db_user = user_table(email=user.email, is_admin=False, first_name=first_name, last_name=last_name, hashed_password=user_hash)

        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)

        return db_user
    
    def delete_user_by_email(self, email: str):
        db_user = self.get_user_by_email(email)
        if not db_user:
            raise NotFoundError("User email not found.")
        query = delete(user_table).where(user_table.email == email.strip())
        response = self._db.execute(query)

        self._db.commit()

        return response
    
    # Genres table queries
    def get_all_music_genre(self, skip: int = 0, limit: int = 100):
        return self._db.query(genre_table).offset(skip).limit(limit).all()
    
    def create_genre(self, genre: Genre):
        name = genre.name
        db_genre = self.get_genre_by_name(name)
        if db_genre:
            raise AlreadyExistsError("Genre already exists.")

        db_genre = genre_table(name=name)

        self._db.add(db_genre)
        self._db.commit()
        self._db.refresh(db_genre)

        return db_genre
    
    def get_genre_by_name(self, name:str):
        if not name or len(name) == 0:
            raise InvalidParameterError("Genre name is required.")
        
        name = name.strip()
        return self._db.query(genre_table).filter(genre_table.name == name).first()
    

    def delete_genre_by_name(self, name: str):
        db_genre = self.get_genre_by_name(name)
        if not db_genre:
            raise NotFoundError("Genre not found.")
        
        query = delete(genre_table).where(genre_table.name == name.strip())
        response = self._db.execute(query)

        self._db.commit()

        return response
    
    def bulk_create_genres(self):
        self._db.bulk_save_objects(genre_list)
        self._db.commit()

        return genre_list
    
    def create_current_user_genres(self, genre_id: List[int], user_id: int):
        arr = []

        for id in genre_id:
            db_instance = personal_genre_table(genre_id=id, user_id=user_id)
            arr.append(db_instance)
        
        self._db.bulk_save_objects(arr)
        self._db.commit()

        return arr
    
    def get_current_user_genres(self, user_id: int):
        results =  self._db.query(personal_genre_table).filter(personal_genre_table.user_id == user_id).all()
        res = []
        for result in results:
            res.append(result.genre)

        return res
    
    def get_all_personal_genres(self, skip: int = 0, limit: int = 100):
        return self._db.query(personal_genre_table).offset(skip).limit(limit).all()

        





        
        
    

        





    
