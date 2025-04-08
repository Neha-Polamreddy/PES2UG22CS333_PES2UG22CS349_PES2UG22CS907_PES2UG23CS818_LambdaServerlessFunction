# backend/models.py
from sqlalchemy import Table, Column, Integer, String
from database import metadata


functions = Table(
    "functions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("route", String, nullable=False),
    Column("language", String, nullable=False),
    Column("timeout", Integer, nullable=False)
)

# <--- Add a blank line here!
