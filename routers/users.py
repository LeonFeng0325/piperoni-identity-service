from fastapi import APIRouter, Depends, HTTPException
from schemas import User
from db_handler import get_db_handler
from exception import InvalidParameterError, AppError, NotFoundError, AlreadyExistsError

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@user_router.post("/", status_code=201)
async def create_new_user(user: User, db_handler=Depends(get_db_handler)):
    try:
        db_handler.create_user(user)
    except InvalidParameterError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except AlreadyExistsError as e:
        raise HTTPException(detail=str(e), status_code=400)
    
    return  {
        "status": "OK",
        "message": "SUCCESS: user created.",
    }


@user_router.get("/all", status_code=200)
async def get_all_users(db_handler=Depends(get_db_handler)):
    try:
        user_list = db_handler.get_users()
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=500)
    
    return {
        "data": user_list,
        "messages": f"SUCCESS: {len(user_list)} users retrieved."
    }


@user_router.get("/{user_email}", status_code=200)
async def get_user_by_email(user_email: str, db_handler=Depends(get_db_handler)):
    try:
        user = db_handler.get_user_by_email(user_email)
        if not user:
            raise NotFoundError("User email does not exist.")
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)
    
    return {
        "data": user,
        "message": "SUCCESS: user retrieved by email."
    }


@user_router.get("/hash/{user_hash}", status_code=200)
async def get_user_by_hash(user_hash: str, db_handler=Depends(get_db_handler)):
    try:
        user = db_handler.get_user_by_hash(user_hash)
        if not user:
            raise NotFoundError("User hash does not exist.")
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)
    
    return {
        "data": user,
        "message": "SUCCESS: user retrieved by hash."
    }


@user_router.get("/{first_name}/{last_name}", status_code=200)
async def get_user_by_full_name(first_name: str, last_name: str, db_handler=Depends(get_db_handler)):
    try:
        user_list = db_handler.get_user_by_full_name(first_name, last_name)
        if len(user_list) == 0:
            raise NotFoundError("User name does not exist.")
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)
    
    return {
        "data": user_list,
        "message": f"SUCCESS: {len(user_list)} users retrieved by name."
    }


@user_router.delete("/hash/{user_hash}", status_code=200)
async def delete_user_by_hash(user_hash: str, db_handler=Depends(get_db_handler)):
    try:
        db_handler.delete_user_by_hash(user_hash)
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)
    
    return {
        "data": "",
        "message": f"SUCCESS: user deleted by hash."
    }


@user_router.delete("/email/{user_email}", status_code=200)
async def delete_user_by_hash(user_email: str, db_handler=Depends(get_db_handler)):
    try:
        db_handler.delete_user_by_email(user_email)
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)
    
    return {
        "data": "",
        "message": f"SUCCESS: user deleted by email."
    }

# TODO: more CRUD endpoints