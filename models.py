from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base
from typing import List

# Database models defined here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False) # User email has to be unique, and this is also user's username
    hashed_password = Column(String, nullable=False) # Hashed using SHA 256 and user specific info
    is_admin = Column(Boolean, default=False) # If user has the admin status, so far unused
    genres: Mapped[List['PersonalGenre']] = relationship(back_populates='user', cascade="all, delete")

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    personalGenres: Mapped[List['PersonalGenre']] = relationship(back_populates="genre", cascade="all, delete")

class PersonalGenre(Base):
    __tablename__ = "personal_genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    user: Mapped[User] = relationship(back_populates="genres")
    genre: Mapped[Genre] = relationship(back_populates="personalGenres")