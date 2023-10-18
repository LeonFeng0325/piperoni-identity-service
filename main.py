import uvicorn
from fastapi import FastAPI
from database import engine
from models import Base
from routers import users, authentication

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication.authentication_router)
app.include_router(users.user_router)


@app.get("/")
async def root():
    return {"message": "Hello There!"}


if __name__ == "__main__": # To start local sever, run ```python main.py```
    uvicorn.run("main:app", reload=True)