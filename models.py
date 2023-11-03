from sqlalchemy import Boolean, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from schemas import CollaborationPreference
from database import Base
from typing import List
from sqlalchemy import Enum

# Database models defined here

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email = mapped_column(String, unique=True, index=True, nullable=False) # User email has to be unique, and this is also user's username
    hashed_password = mapped_column(String, nullable=False) # Hashed using SHA 256 and user specific info
    oauth2: Mapped[Boolean] = mapped_column(Boolean, default=False) # is user oauth2 or not
    genres: Mapped[List['PersonalGenre']] = relationship(back_populates='user', cascade="all,delete")
    instruments: Mapped[List['PersonalInstrument']] = relationship(back_populates='', cascade="all,delete")
    details: Mapped['UserDetail'] = relationship(back_populates='user', cascade="all,delete")


class UserDetail(Base):
    __tablename__ = "user_details"
    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id =  mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    first_name = mapped_column(String)
    last_name = mapped_column(String)
    title = mapped_column(String)
    description = mapped_column(String)
    preference: Mapped[CollaborationPreference] = mapped_column(Enum(CollaborationPreference), default=CollaborationPreference.no_preference)
    address = mapped_column(String)
    user: Mapped['User'] = relationship(back_populates="details")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    personalGenres: Mapped[List['PersonalGenre']] = relationship(back_populates="genre", cascade="all,delete")

class PersonalGenre(Base):
    __tablename__ = "personal_genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="genres")
    genre: Mapped[Genre] = relationship(back_populates="personalGenres")

    __table_args__  = (UniqueConstraint('user_id', 'genre_id', name='unique_personal_genre'),)


class Instrument(Base):
    __tablename__ = "instruments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    personalInstruments: Mapped[List['PersonalInstrument']] = relationship(back_populates='instrument', cascade='all,delete')


class PersonalInstrument(Base):
    __tablename__ = "personal_instruments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates='instruments')
    instrument: Mapped[Instrument] = relationship(back_populates='personalInstruments')

    __table_args__ = (UniqueConstraint('user_id', 'instrument_id', name='unique_personal_instrument'),)