# Project Stack

- This backend web service is built using Python 3.9, [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/) as ORM, and PostgreSQL as database
- I use SQLAlchemy because I suck at writing raw sql, and SQLAlchemy, as an ORM, enables us to write sql statements with pure python code.
- Maybe will add redis if I have time

# Dependency

- All dependencies are listed inside requirements.txt.
- To install all dependencies for this project, first create a python virtual environment with Python 3.9 in the root of your local repo, and then run ```pip install -r requirements.txt```
- Install Docker and docker desktop to your machine for local development purpose.

# Local Development

- First, run ```docker-compose up -d``` to start docker containers. A PostgreSQL container and a pgAdmin container will be created inside docker containers.
- To use pgAdmin, go to ```http://localhost:5555```. To login, use the credentials inside the docker-compose file.
- Second, run ```uvicorn main:app --reload``` to start the web server locally.
- App should have hot reload ability out of the box. If something is updating properly, just refresh the page.

