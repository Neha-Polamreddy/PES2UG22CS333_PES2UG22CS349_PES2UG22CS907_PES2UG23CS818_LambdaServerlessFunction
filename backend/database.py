# backend/database.py
from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./functions.db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


W292 no newline at end of file