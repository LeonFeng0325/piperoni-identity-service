from fastapi import APIRouter, Depends, HTTPException, status
from auth.auth_token import create_access_token, oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from schemas import User, Token
from handlers.handlers import get_db_handler
from exception import InvalidParameterError, AlreadyExistsError
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
import requests
from jwt.algorithms import RSAAlgorithm
from time import time
import json
import os


ACCESS_TOKEN_EXPIRE_MINUTES = 60
APPLE_PUBLIC_KEY_URL = "https://appleid.apple.com/auth/keys"
APPLE_PUBLIC_KEY = None
APPLE_KEY_CACHE_EXP = 60 * 60 * 24
APPLE_LAST_KEY_FETCH = 0

authentication_router = APIRouter(
    tags=["authentication"],
)

def fetch_apple_public_key():
    # Check to see if the public key is unset or is stale before returning
    global APPLE_LAST_KEY_FETCH
    global APPLE_PUBLIC_KEY

    if (APPLE_LAST_KEY_FETCH + APPLE_KEY_CACHE_EXP) < int(time()) or APPLE_PUBLIC_KEY is None:
        key_payload = requests.get(APPLE_PUBLIC_KEY_URL).json()
        APPLE_PUBLIC_KEY = RSAAlgorithm.from_jwk(json.dumps(key_payload["keys"][0]))
        APPLE_LAST_KEY_FETCH = int(time())

    return APPLE_PUBLIC_KEY


def decode_apple_user_token(apple_user_token):
    public_key = fetch_apple_public_key()

    try:
        token = jwt.decode(apple_user_token, public_key, audience=os.getenv("APPLE_APP_ID"), algorithm="RS256")
    except jwt.exceptions.ExpiredSignatureError as e:
        raise Exception("That token has expired.")
    except jwt.exceptions.InvalidAudienceError as e:
        raise Exception("That token's audience did not match.")
    except Exception as e:
        print(e)
        raise Exception("An unexpected error occurred.")

    return token


# Helper function to verify if the incoming HTTP has the valid JWT as the bearer token.
# A JWT is valid if it is not expired and can be correctly decoded and match with our database data.
# JWT is signed by a secret key and should be keep safe.
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


# Hack: need to rework in future
@authentication_router.get("/google_oauth/{email}", status_code=status.HTTP_200_OK, response_model=Token)
async def google_login_for_access_token(email:str, db_handler=Depends(get_db_handler)):
    user = db_handler.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
