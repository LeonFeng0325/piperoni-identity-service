from fastapi import APIRouter, Depends, HTTPException
from schemas import User
from db_handler import get_db_handler
from exception import InvalidParameterError, AppError

router = router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User Not found"}, 403: {"description": "Operation forbidden"}},
)

@router.post("/", status_code=201)
async def create_new_user(user: User, db_handler=Depends(get_db_handler)):
    try:
        db_handler.create_user(user)
        return  {
            "status": "OK",
            "message": "SUCCESS: user created.",
        }
    except InvalidParameterError as e:
        raise HTTPException(detail=str(e), status_code=400)
    
@router.get("/all", status_code=200)
async def get_all_users(db_handler=Depends(get_db_handler)):
    try:
        user_list = db_handler.get_users()
        return {
            "data": user_list,
            "messages": "SUCCESS: all users retrieved."
        }
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=500)

