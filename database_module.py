from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from dotenv import load_dotenv
import os
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)

# Creating a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DBSession:
    def __init__(self):
        self._session = None

    def __enter__(self):
        self._session = SessionLocal()
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        if self._session:
            self._session.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
