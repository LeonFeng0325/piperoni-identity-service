from models import Genre, User, PersonalGenre, Instrument, PersonalInstrument
from auth.auth_password import get_password_hash
# Define some data when database resets

user_list = [
    User(first_name="Rishabh", last_name="Poikayil", is_admin=False, hashed_password=get_password_hash("password"), email="rishabh_poikayil@ucsb.edu"),
    User(first_name="Leon", last_name="Feng", is_admin=False, hashed_password=get_password_hash("password"), email="b_feng@ucsb.edu"),
    User(first_name="Aviv", last_name="Samet", is_admin=False, hashed_password=get_password_hash("password"), email="aviv@ucsb.edu"),
    User(first_name="Kirill", last_name="Aristarkhov", is_admin=False, hashed_password=get_password_hash("password"), email="kya@ucsb.edu"),
    User(first_name="Andy", last_name="Gonzalez", is_admin=False, hashed_password=get_password_hash("password"), email="andysgonzalez@ucsb.edu")
]

genre_list = [
    Genre(name="Classical"), 
    Genre(name="Hip Hop"), 
    Genre(name="Rock"), 
    Genre(name="Jazz"), 
    Genre(name="Indie"),
    Genre(name="Metal"),
    Genre(name="Pop"),
    Genre(name="Electronic"),
    Genre(name="Blues"),
    Genre(name="Rap"),
    Genre(name="Punk"),
    Genre(name="Folk"),
    Genre(name="World Music"),
    Genre(name="Gospel"),
    Genre(name="R&B")
]

personal_genre_list = [
    PersonalGenre(user_id=1, genre_id=1),
    PersonalGenre(user_id=1, genre_id=3),
    PersonalGenre(user_id=1, genre_id=5),
    PersonalGenre(user_id=2, genre_id=2),
    PersonalGenre(user_id=2, genre_id=4),
    PersonalGenre(user_id=2, genre_id=6),
]

instrument_list = [
    Instrument(name="Guitar"),
    Instrument(name="Cello"),
    Instrument(name="Banjo"),
    Instrument(name="Bass"),
    Instrument(name="Harp"),
    Instrument(name="Saxophone"),
    Instrument(name="Clarinet"),
    Instrument(name="Electric Keyboard"),
    Instrument(name="Glass Harmonica"),
    Instrument(name="Accordion"),
    Instrument(name="Piano"),
    Instrument(name="Drum"),
    Instrument(name="Tube"),
]

personal_instrument_list = [
    PersonalInstrument(user_id=1, instrument_id=3),
    PersonalInstrument(user_id=1, instrument_id=5),
    PersonalInstrument(user_id=1, instrument_id=7),
    PersonalInstrument(user_id=2, instrument_id=1),
    PersonalInstrument(user_id=2, instrument_id=2),
    PersonalInstrument(user_id=2, instrument_id=6)
]
