from fastapi import Depends
from db_handler import DBHandler
from database import get_db

def get_db_handler(db=Depends(get_db)):
    return DBHandler(db)