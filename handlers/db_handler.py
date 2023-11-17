from auth.auth_password import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from models import User as user_table, Genre as genre_table, PersonalGenre as personal_genre_table, Instrument as instrument_table, PersonalInstrument as personal_instrument_table, UserDetail as user_detail_table
from schemas import User, Genre, Instrument
from exception import AlreadyExistsError, InvalidParameterError, NotFoundError
from utils.email_verification import is_valid_email
from auth.auth_password import verify_password
from typing import List

# DB Handler class that handles all database interactions
class DBHandler:

    def __init__(self, db: Session) -> None:
        super().__init__()
        self._db = db
    
    def get_user_by_email(self, email: str):
        return self._db.query(user_table).filter(user_table.email == email.strip()).first()
    
    def get_users(self, skip: int = 0, limit: int = 100):
        return self._db.query(user_table).offset(skip).limit(limit).all()
    
    def get_all_users_genres(self):
        users = self._db.query(user_table).all()
        return [{"user_id": user.id, "genres": [genre.genre.name for genre in user.genres]} for user in users]

    def get_all_users_instruments(self):
        users = self._db.query(user_table).all()
        return [{"user_id": user.id, "instruments": [instrument.instrument.name for instrument in user.instruments]} for user in users]

    def authenticate_user(self, email: str, password: str): # custom auth
        db_user = self.get_user_by_email(email)
        if not db_user or db_user.oauth2:
            return False
        if not verify_password(password, db_user.hashed_password):
            return False
        return db_user
    
    def create_user(self, user: User, oauth: bool):
        user_email = user.email.strip()
        password = user.password.strip()

        db_user = self.get_user_by_email(user_email)
        # Sanity check
        if db_user:
            raise AlreadyExistsError("Email already exists.")
        if not user_email or len(user_email) == 0:
            raise InvalidParameterError("Email is required.")
        if not is_valid_email(user_email):
            raise InvalidParameterError("Please provide a valid email.")
        if not password or len(password) == 0:
            raise InvalidParameterError("Password is required")

        user_hash = get_password_hash(password) # Unique to each user
        db_user = user_table(email=user.email, hashed_password=user_hash, oauth2=oauth)

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
    def get_all_music_genres(self, skip: int = 0, limit: int = 100):
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
    

    def delete_current_user_genre(self, user_id: int, genre_id: int):
        result = self._db.query(personal_genre_table).where(personal_genre_table.user_id==user_id, personal_genre_table.genre_id==genre_id).first()
        if not result:
            raise NotFoundError("Current user does not have the specified genre.")

        query = delete(personal_genre_table).where(personal_genre_table.genre_id == genre_id, personal_genre_table.user_id==user_id)
        self._db.execute(query)
        self._db.commit()
        
        return
    
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

    # Instrument table queries
    def get_all_instruments(self, skip: int = 0, limit: int = 100):
        return self._db.query(instrument_table).offset(skip).limit(limit).all()
    
    def get_instrument_by_name(self, name: str):
        if not name or len(name) == 0:
            raise InvalidParameterError("Instrument name is required.")
        
        name = name.strip()
        return self._db.query(instrument_table).filter(instrument_table.name == name).first()
    

    def create_instrument(self, instrument: Instrument):
        instrument_name = instrument.name
        db_instrument = self.get_instrument_by_name(instrument_name)
        if db_instrument:
            raise AlreadyExistsError("Instrument already exists")
        
        db_instrument = instrument_table(name=instrument_name)
        self._db.add(db_instrument)
        self._db.commit()
        self._db.refresh(db_instrument)

        return db_instrument
    
    def delete_instrument_by_name(self, instrument_name: str):
        db_instrument = self.get_instrument_by_name(instrument_name)
        if not db_instrument:
            raise NotFoundError("Instrument not found.")
        
        query = delete(instrument_table).where(instrument_table.name == instrument_name)
        self._db.execute(query)
        self._db.commit()

        return
    
    def delete_current_user_instrument_by_id(self, user_id: int, instrument_id: int):
        result = self._db.query(personal_instrument_table).where(personal_instrument_table.user_id == user_id, personal_instrument_table.instrument_id == instrument_id).first()
        if not result:
            raise NotFoundError("Current user doesn't have specified instrument.")

        query = delete(personal_instrument_table).where(personal_instrument_table.instrument_id == instrument_id, personal_instrument_table.user_id== user_id)
        self._db.execute(query)
        self._db.commit()

        return

    def create_personal_instruments(self, user_id: int, instrument_id: List[int]):
        arr = []
    
        for id in instrument_id:
            db_instance = personal_instrument_table(user_id=user_id, instrument_id=id)
            arr.append(db_instance)
        
        self._db.bulk_save_objects(arr)
        self._db.commit()

        return arr
        return db_personal_instrument
    
    def get_current_user_instruments(self, user_id):
        results =  self._db.query(personal_instrument_table).filter(personal_instrument_table.user_id == user_id).all()
        res = []
        for result in results:
            res.append(result.instrument)

        return res
    
    # Personal detail table queries
    def get_current_user_personal_details(self, user_id: int):
        return self._db.query(user_detail_table).filter(user_detail_table.user_id == user_id).first()
    
    def get_all_user_personal_details(self):
        return self._db.query(user_detail_table).all()
    
    
    def create_current_user_personal_details(self, first_name: str, last_name: str, title: str, description: str, preference, address: str, user_id: int):
        db_user = self.get_current_user_personal_details(user_id)
        if db_user:
            raise AlreadyExistsError("User details have already been created.")
        
        db_instance = user_detail_table(first_name=first_name, last_name=last_name, user_id=user_id, title=title, description=description, preference=preference, address=address)
        self._db.add(db_instance)
        self._db.commit()
        self._db.refresh(db_instance)

        return db_instance
    
    def update_current_user_personal_details_fields(self, field: str, data: str, user_id: int):
        db_user_details = self.get_current_user_personal_details(user_id)
        if not db_user_details:
            raise NotFoundError("User has not initialized personal details.")
        
        query = update(user_detail_table).where(user_detail_table.user_id == user_id).values({field: data})

        self._db.execute(query)
        self._db.commit()
        updated_user_detail = self.get_current_user_personal_details(user_id)

        return updated_user_detail