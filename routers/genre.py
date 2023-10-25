from fastapi import APIRouter, Depends, HTTPException, status
from handlers.handlers import get_db_handler
from routers.authentication import get_current_user
from exception import  AppError, NotFoundError
from schemas import Genre, User
from typing import List

genre_router = APIRouter(
    prefix="/api/genres",
    tags=["genres"]
)


@genre_router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_genres(db_handler=Depends(get_db_handler)):
    try:
        genre_list = db_handler.get_all_music_genre()
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return {
        "data": genre_list,
        "messages": f"SUCCESS: {len(genre_list)} genres retrieved."
    }


@genre_router.get("/me", status_code=status.HTTP_200_OK)
async def get_personal_genres(db_handler=Depends(get_db_handler), current_user = Depends(get_current_user)):
    try:
        current_user_id = current_user.id
        db_personal_list = db_handler.get_current_user_genres(current_user_id)
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return {
        "data": db_personal_list,
        "messages": f"SUCCESS: genres retrieved for current user."
    }


@genre_router.get("/{genre_name}", status_code=status.HTTP_200_OK)
async def get_genre_by_name(genre_name: str, db_handler=Depends(get_db_handler)):
    try:
        db_genre = db_handler.get_genre_by_name(genre_name)
        if not db_genre:
            raise NotFoundError("Genre does not exist")
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "data": db_genre,
        "message": "SUCCESS: genre retrieved by name."
    }


@genre_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_genre(genre: Genre, db_handler=Depends(get_db_handler)):
    try:
        db_genre = db_handler.create_genre(genre)
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return {
        "data": db_genre,
        "messages": f"SUCCESS:  genre created."
    }


@genre_router.post("/batch", status_code=status.HTTP_201_CREATED, description="Bulk created a list of genres")
async def batch_create_genre(db_handler=Depends(get_db_handler)):
    try:
        db_genre_list = db_handler.bulk_create_genres()
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return {
        "data": db_genre_list,
        "messages": f"SUCCESS: {len(db_genre_list)}  genre created."
    }


@genre_router.delete("/{genre_name}", status_code=status.HTTP_200_OK)
async def delete_genre(genre_name: str, db_handler=Depends(get_db_handler)):
    try:
        db_handler.delete_genre_by_name(genre_name)
    except NotFoundError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)
    
    return {
        "data": "",
        "message": f"SUCCESS: genre deleted by name."
    }


@genre_router.post("/me", status_code=status.HTTP_201_CREATED)
async def create_personal_genres(genre_id: List[int], db_handler=Depends(get_db_handler), current_user: User = Depends(get_current_user)):
    try:
        current_user_id = current_user.id
        db_genre = db_handler.create_current_user_genres(genre_id, current_user_id)
    except AppError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return {
        "data": db_genre,
        "messages": f"SUCCESS:  genre created."
    }