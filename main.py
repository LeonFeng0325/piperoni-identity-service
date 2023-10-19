import uvicorn
from fastapi import FastAPI
from database import engine
from models import Base
from routers import users, authentication

Base.metadata.create_all(bind=engine) # Create database tables on server start.

app = FastAPI()

# Register API endpoints
app.include_router(authentication.authentication_router)
app.include_router(users.user_router)


@app.get("/")
async def index():
    return {"message": "Hello There!"}


@app.get("/reset")
async def reset(): # This endpoint will drop all db tables and recreate them in database from scratch. This is a hack so we don't need to do database migrations.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__": # The entry point of the application. To start local sever, run ```python main.py```
    uvicorn.run("main:app", reload=True)