import os

from fastapi import APIRouter, UploadFile, Depends, HTTPException, status, Response
from routers.authentication import get_current_user
from handlers.handlers import get_db_handler

router = APIRouter(prefix="/api/files", tags=["files"])

@router.post("/upload")
async def upload_file(file: UploadFile, current_user=Depends(get_current_user), db_handler=Depends(get_db_handler)):
    if file.content_type != "image/png":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a png image.")
    contents = await file.read()
    filepath = f"/pics/{current_user.id}.png"

    # Have to try to create the directory first
    # https://stackoverflow.com/questions/23793987/write-a-file-to-a-directory-that-doesnt-exist
    try:
        os.makedirs(os.path.dirname(filepath))
    except FileExistsError:
        pass
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    with open(filepath, "wb") as f:
        f.write(contents)

    db_handler.update_current_user_personal_details_fields("profile_picture", filepath, current_user.id)

    return {"filepath": filepath}

@router.get("/profile")
def get_profile_pic(current_user=Depends(get_current_user), db_handler=Depends(get_db_handler)):
    user_details = db_handler.get_current_user_personal_details(current_user.id)
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User details not found.")
    if not user_details.profile_picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile picture not found.")
    
    picture_file = open(user_details.profile_picture, "rb")

    picture_bytes = picture_file.read()

    return Response(content=picture_bytes, media_type="image/png")
    