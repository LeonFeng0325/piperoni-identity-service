from database import engine
from models import Base

def reset_db():
    Base.metadata.drop_all(bind=engine)

# Run this script to clean all database data and table and start fresh for local dev purpose, so I don't have to run db migration when changing db schema because I am lazy
if __name__ == "__main__":
    reset_db()