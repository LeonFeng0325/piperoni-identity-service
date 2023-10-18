from fastapi import APIRouter, Depends, HTTPException, status
from auth_token import create_access_token, oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from schemas import User, Token
from handlers import get_db_handler
from exception import InvalidParameterError, AlreadyExistsError
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 60

authentication_router = APIRouter(
    tags=["authentication"],
)


def get_current_user(token: str = Depends(oauth2_scheme), db_handler=Depends(get_db_handler)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try: 
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub")
            if not user_email:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = db_handler.get_user_by_email(payload.get("sub"))
        if not user:
            raise credentials_exception
    
        return user


@authentication_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: User, db_handler=Depends(get_db_handler)):
    try:
        db_handler.create_user(user)
    except InvalidParameterError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    except AlreadyExistsError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    
    return  {
        "status": "OK",
        "message": "SUCCESS: user created.",
    }


@authentication_router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_handler=Depends(get_db_handler)):
    user = db_handler.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}