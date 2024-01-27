from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database_module import *
from middleware_module import *
from basemodels_module import *
from fastapi import BackgroundTasks
from Authentication import get_current_user, create_access_token, refresh_tokens, verify_refresh_token, create_both_tokens
from fastapi.responses import JSONResponse
from functions import *

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if debug_mode:
    app.middleware("http")(custom_logging)

#------------------------- Admin access only endpoints (needs isAdmin checker) -------------------------
@app.post("/revoke-token")
async def revoke_token(token: str):
    try:
        refresh_tokens.remove(token)
    except KeyError:
        pass
    return {"message": "Token revoked"}

# ------------------------- COMMON -------------------------
@app.post("/register", response_model=UserDBCreate)
async def create_user(user: UserDBCreate, db: Session = Depends(get_db)):
    try:
        if user_exists(user.model_dump()['phone']):
            return JSONResponse(status_code=400, content={"message": "User already exists."})
        else:
            db_user = UserDB(**user.model_dump())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            amenity_id = map_user_type_to_amenity_id(db_user.user_type)
            user_feature_association = UserFeaturesAssociation(user_id=db_user.user_id, amenity_id=amenity_id)
            db.add(user_feature_association)
            db.commit()

            token, refresh_token = create_both_tokens(db_user.phone, db_user.user_id)
            response_data = {"message": "User added successfully.", "access_token": token,  "token_type": "bearer", "refresh_token": refresh_token}
            return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        db.rollback()
        response_data = {'message': 'Error adding user to the database:' + str(e)}
        return JSONResponse(content=response_data, status_code=500)
    finally:
        db.close()

@app.post("/token")
async def login(request_data: dict, db: Session = Depends(get_db)):
    phone = request_data.get("phone_number")
    user = db.query(UserDB).filter(UserDB.phone == phone).first()
    if user:
        token, refresh_token = create_both_tokens(request_data.get("phone_number"), user.user_id)
        return {"access_token": token,  "token_type": "bearer", "refresh_token": refresh_token}
    else:
        raise HTTPException(status_code=401, detail="User does not exist.")

@app.post("/refresh-access-token")
async def refresh_token(request_data: dict):
    refresh_token = request_data.get("refresh_token")
    if refresh_token not in refresh_tokens:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    loggedin_user, permissions = verify_refresh_token(refresh_token)
    if loggedin_user and permissions:
        access_token = create_access_token(data={"sub": loggedin_user, "permissions" : permissions})
        return {"access_token": access_token, "token_type": "bearer"}

@app.get("/verify-user", response_model=dict)
async def verify_user(current_user: dict = Depends(get_current_user)):
    return {"message": current_user['username'], "message2": current_user['contact']}

#test endpoint
@app.get("/check-admin-demo/{admin_id}")
def test(admin_id: int):
    if admin_id != 1:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"admin_id": admin_id}
