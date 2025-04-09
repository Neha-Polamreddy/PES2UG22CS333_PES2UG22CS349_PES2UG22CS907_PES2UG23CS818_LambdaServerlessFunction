# backend/database.py
from sqlalchemy import create_engine, MetaData
from databases import Database
import os


# PostgreSQL connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/lambda_functions"
)

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)


# <--- Add a blank line here!
