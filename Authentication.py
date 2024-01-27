from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from dotenv import load_dotenv
import os
from typing import List, Union

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

refresh_tokens = set()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ACCESSALGORITHM = os.getenv("ALGORITHM")
REFRESHALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    try:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ACCESSALGORITHM)
    except JWTError as e:
        raise HTTPException(status_code=500, detail=f"Error encoding access token: {str(e)}")

def create_refresh_token(phone_number: str, uuid: str):
    permissions = ["WRITE"]  # Fetch from db based on username/phonenumber
    refresh_token_data = {
        "uuid": uuid,
        "contact": phone_number,
        "permissions": permissions,
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }
    try:
        refresh_token = jwt.encode(refresh_token_data, REFRESH_SECRET_KEY, algorithm=REFRESHALGORITHM)
        refresh_tokens.add(refresh_token)
        return permissions, refresh_token
    except JWTError as e:
        raise HTTPException(status_code=500, detail=f"Error encoding refresh token: {str(e)}")

def create_both_tokens(phone_number: str, uuid: str):
    permissions, refresh_token = create_refresh_token(phone_number, uuid)
    access_token = create_access_token(data={"sub": uuid, "contact": phone_number, "permissions": permissions})
    return access_token, refresh_token

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ACCESSALGORITHM])
        uuid: str = payload.get("sub")
        contact: str = payload.get("contact")
        permissions: List[Union[str, None]] = payload.get("permissions")
        if not permissions:
            raise credentials_exception
        return {"uuid": uuid, "contact": contact}
    except JWTError as e:
        raise credentials_exception from e  # Re-raise with more details

def verify_refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[REFRESHALGORITHM])
        return payload.get("uuid"), payload.get("permissions")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")