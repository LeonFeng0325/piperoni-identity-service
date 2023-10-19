from fastapi import APIRouter, Depends, HTTPException, status
from handlers.handlers import get_db_handler
from exception import  AppError, NotFoundError
from schemas import User
from routers.authentication import get_current_user


user_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@user_router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_users(db_handler=Depends(get_db_handler)):
    try:
        user_list = db_handler.get_users()
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return {
        "data": user_list,
        "messages": f"SUCCESS: {len(user_list)} users retrieved."
    }


@user_router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.get("/{user_email}", status_code=status.HTTP_200_OK)
async def get_user_by_email(user_email: str, db_handler=Depends(get_db_handler), current_user: User = Depends(get_current_user)):
    try:
        user = db_handler.get_user_by_email(user_email)
        if not user:
            raise NotFoundError("User email does not exist.")
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "data": user,
        "message": "SUCCESS: user retrieved by email."
    }


@user_router.get("/{first_name}/{last_name}", status_code=status.HTTP_200_OK)
async def get_user_by_full_name(first_name: str, last_name: str, db_handler=Depends(get_db_handler), current_user: User = Depends(get_current_user)):
    try:
        user_list = db_handler.get_user_by_full_name(first_name, last_name)
        if len(user_list) == 0:
            raise NotFoundError("User name does not exist.")
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "data": user_list,
        "message": f"SUCCESS: {len(user_list)} users retrieved by name."
    }


@user_router.delete("/email/{user_email}", status_code=status.HTTP_200_OK)
async def delete_user_by_email(user_email: str, db_handler=Depends(get_db_handler), current_user: User = Depends(get_current_user)):
    try:
        db_handler.delete_user_by_email(user_email)
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "data": "",
        "message": f"SUCCESS: user deleted by email."
    }
