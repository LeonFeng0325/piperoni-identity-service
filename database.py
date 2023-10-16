from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Piperoni Identity service uses PostgreSQL to persistent storage to hold all user authentication data
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:secret@postgres:5432/identity_database"

# Create SQLAlchemy db engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()