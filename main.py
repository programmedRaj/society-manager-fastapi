from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database_module import *
from middleware_module import *
from basemodels_module import *
from fastapi import BackgroundTasks

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

@app.get("/check-admin-demo/{admin_id}")
def test(admin_id: int):
    if admin_id != 1:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"admin_id": admin_id}
