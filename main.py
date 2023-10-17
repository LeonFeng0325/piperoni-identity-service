from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from database import engine
from models import Base
from routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(users.user_router)


@app.get("/")
async def root():
    return {"message": "Hello There!"}